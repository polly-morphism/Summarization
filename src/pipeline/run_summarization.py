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
        start = time.time()
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


####
# EXAMPLE
####

# text = """ WASHINGTON — In a six-page invective to House Speaker Nancy Pelosi, President Donald Trump contended he has been more wronged in the impeachment proceedings than even the 17th-century women who were hanged based on dreams, visions and confessions elicited by torture.\n
#
# "More due process was afforded to those accused in the Salem Witch Trials," the president wrote. \n
#
# His allies have made similar arguments, though not quite so hyperbolic. They said the president has been railroaded based on hearsay evidence. They argued he has been deprived of the right to face his accusers. They claimed the House's impeachment proceedings would not have been allowed in a court of law. \n
#
# But legal experts say this criticism, peppered with terms borrowed from criminal proceedings, is based on a misinterpretation of what the Constitution says about impeachment and how much protection it gives the president./n
#
# The answer: Not much.\n
#
# Like Bill Clinton in the 1990s and Andrew Johnson more than a century earlier, Trump does not have the same constitutional protection afforded to a criminal defendant, they said. \n
#
# "The president of the United States takes the presidency conditioned on the fact that he may be subject to impeachment," said Michael Gerhardt, a University of North Carolina law professor. "He has no entitlement to demand due process." \n
# """
# arguments = Namespace(
#     alpha=0.95,
#     batch_size=4,
#     beam_size=5,
#     block_trigram=True,
#     compute_rouge=False,
#     documents_dir="./news_sum",
#     max_length=300,
#     min_length=200,
#     no_cuda=False,
#     summaries_output_dir="./news_sum",
# )
#
# # Select device (distibuted not available)
# arguments.text = text
# arguments.device = torch.device("cuda")
# arguments.finalize()
# summarizer = Summarization()
