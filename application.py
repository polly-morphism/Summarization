import os
from flask import Flask

from conf.app_config import get_config
from src.pipeline.summarizer import Summarization

base_dir = os.path.dirname(__file__)
conf_dir = os.path.join(base_dir, "conf")

app = Flask(__name__)
app.config.from_object(get_config())
app.config.update({"BASE_DIR": base_dir})
app.config.update({"CONF_FOLDER": os.path.join(base_dir, "conf")})

summarizer = Summarization()
