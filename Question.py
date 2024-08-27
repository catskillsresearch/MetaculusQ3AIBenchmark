from pony.orm import *
from datetime import date
from db import db

class Question(db.Entity):
    
    id = PrimaryKey(int, auto=False)
    ask_date = Required(date)
    active_state = Required(str)
    resolution = Optional(float)
    title = Required(str)
    background = Optional(str)
    fine_print = Optional(str)
    resolution_criteria = Required(str)
    json = Required(Json)
