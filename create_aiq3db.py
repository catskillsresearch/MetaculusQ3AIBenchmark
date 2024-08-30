import json
from pony.orm import *
from datetime import date
from tqdm import tqdm
from db import db
from Question import Question

db.bind(provider='sqlite', filename='/home/catskills/Desktop/MetaculusQ3AIBenchmark/q3ai.db', create_db=True)

db.generate_mapping(create_tables=True)

from history import *

with db_session:
    for key in history:
        for qid in history[key]:
            with open(f'questions/{qid}.json', 'r') as f:
                qj = json.load(f)
                publish_time =  date.fromisoformat(qj['publish_time'][0:10])
                q = Question(id = qj['id'],
                        ask_date = publish_time,
                        active_state = qj["active_state"],
                        resolution = qj["resolution"],
                        title = qj["title"],
                        background = qj["description"],
                        fine_print = qj["fine_print"],
                        resolution_criteria = qj["resolution_criteria"],
                        json = qj)