import time
from transformers import BertTokenizer
import argparse
import os
import sys
from collections import namedtuple
from input_reader import Namespace

import torch
from torch.utils.data import DataLoader, SequentialSampler
from tqdm import tqdm

from .modeling_bertabs import BertAbs, build_predictor
from transformers import BertTokenizer
from .utils_summarization import (
    SummarizationDataset,
    build_mask,
    compute_token_type_ids,
    encode_for_summarization,
    fit_to_block_size,
)

import os

import requests
from bson import ObjectId
from requests import Response

from src.database import mongo_db
from src.tasks import celery
from typing import Dict, Any, List, Union


Batch = namedtuple(
    "Batch", ["document_names", "batch_size", "src", "segs", "mask_src", "tgt_str"]
)


def format_summary(translation):
    """ Transforms the output of the `from_batch` function
    into nicely formatted summaries.
    """
    raw_summary, _, _ = translation
    summary = (
        raw_summary.replace("[unused0]", "")
        .replace("[unused3]", "")
        .replace("[PAD]", "")
        .replace("[unused1]", "")
        .replace(r" +", " ")
        .replace(" [unused2] ", ". ")
        .replace("[unused2]", "")
        .strip()
    )

    return summary


def build_data_iterator(args, tokenizer):
    dataset = load_and_cache_examples(args, tokenizer)
    sampler = SequentialSampler(dataset)

    def collate_fn(data):
        return collate(data, tokenizer, block_size=512, device=args.device)

    iterator = DataLoader(
        dataset, sampler=sampler, batch_size=args.batch_size, collate_fn=collate_fn,
    )

    return iterator


def load_and_cache_examples(args, tokenizer):
    dataset = SummarizationDataset(text=args.text)
    return dataset


def collate(data, tokenizer, block_size, device):
    """ Collate formats the data passed to the data loader.

    In particular we tokenize the data batch after batch to avoid keeping them
    all in memory. We output the data as a namedtuple to fit the original BertAbs's
    API.
    """
    data = [x for x in data if not len(x[1]) == 0]  # remove empty_files
    names = [name for name, _, _ in data]
    summaries = [" ".join(summary_list) for _, _, summary_list in data]

    encoded_text = [
        encode_for_summarization(story, summary, tokenizer)
        for _, story, summary in data
    ]
    encoded_stories = torch.tensor(
        [
            fit_to_block_size(story, block_size, tokenizer.pad_token_id)
            for story, _ in encoded_text
        ]
    )
    encoder_token_type_ids = compute_token_type_ids(
        encoded_stories, tokenizer.cls_token_id
    )
    encoder_mask = build_mask(encoded_stories, tokenizer.pad_token_id)

    batch = Batch(
        document_names=names,
        batch_size=len(encoded_stories),
        src=encoded_stories.to(device),
        segs=encoder_token_type_ids.to(device),
        mask_src=encoder_mask.to(device),
        tgt_str=summaries,
    )

    return batch


class Summarization:
    def __init__(self):

        self.tokenizer = BertTokenizer.from_pretrained(
            "bert-base-uncased", do_lower_case=True
        )
        self.model = BertAbs.from_pretrained("bertabs-finetuned-cnndm")
        if torch.cuda.is_available():
            self.model.to("cuda")
        else:
            self.model.to("cpu")
        self.model.eval()

    def evaluate(self, args):
        symbols = {
            "BOS": self.tokenizer.vocab["[unused0]"],
            "EOS": self.tokenizer.vocab["[unused1]"],
            "PAD": self.tokenizer.vocab["[PAD]"],
        }

        args.result_path = ""
        args.temp_dir = ""

        data_iterator = build_data_iterator(args, self.tokenizer)
        print(data_iterator)
        predictor = build_predictor(args, self.tokenizer, symbols, self.model)
        result = []
        for batch in tqdm(data_iterator):
            batch_data = predictor.translate_batch(batch)
            translations = predictor.from_batch(batch_data)
            summaries = [format_summary(t) for t in translations]
            result.append(summaries)
        return result


@celery.task(ignore_result=True, name="get_summary")
def get_summary(document_id: str) -> None:
    selected_fields: Dict[str, int] = {
        "title": 1,
    }
    document: Dict[str, Any] = mongo_db.news.find_one(
        {"_id": ObjectId(document_id)}, selected_fields
    )

    if document:
        url = os.getenv("SUMMARIZER_API_URL")
        headers = {"Content-type": "application/json"}
        json_data: Dict[str, str] = {"text": document["content"]}
        response: Response = requests.post(url=url, json=json_data, headers=headers)

        if response.status_code == requests.codes.OK:
            entities: List[Dict[str, Union[str, int, float]]] = list(response.json())
            data = {"summary": entities}
            mongo_db.news.update({"_id": ObjectId(document_id)}, {"$set": data})
