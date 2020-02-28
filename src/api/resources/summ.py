from flask import Response, jsonify
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from input_reader import Namespace
import torch
from application import summarizer


class SUMM(Resource):
    request_args = {
        "text": fields.Str(required=True),
    }

    @use_args(request_args)
    def post(self, *args, **kwargs) -> Response:
        text = args[0].get("text", None)
        if not text:
            resp = jsonify({"error": "You must specify text parameter"})
            resp.status_code = 449
            return resp
        arguments = Namespace(
            alpha=0.95,
            batch_size=4,
            beam_size=5,
            block_trigram=True,
            compute_rouge=False,
            documents_dir="./news_sum",
            max_length=200,
            min_length=50,
            no_cuda=False,
            summaries_output_dir="./news_sum",
        )

        # Select device (distibuted not available)
        arguments.text = text
        arguments.device = torch.device("cuda")
        arguments.finalize()

        result = summarizer.evaluate(arguments)

        resp = jsonify(result)
        resp.status_code = 200
        return resp
