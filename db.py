from pony.orm import Database

db = Database()

def start_db():
    db.bind(provider='sqlite', filename='/home/catskills/Desktop/MetaculusQ3AIBenchmark/q3ai.db')
    db.generate_mapping(create_tables=False)