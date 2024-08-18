import json
from datetime import datetime
from metaculus import post_question_prediction, post_question_comment, get_question_details

def row_exists(row_id):
    conn = sqlite3.connect('q3ai.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM ifp WHERE id = ?", (row_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def update_resolved_field(database, new_value, row_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    # Update the resolved field for the specified row
    cursor.execute('''
        UPDATE ifp
        SET resolution = ?
        WHERE id = ?
    ''', (new_value, row_id))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

class IFP:

    forecast_fields = ['question_id',
                       'title',
                       'feedback',
                       'resolution_criteria', 
                       'background', 
                       'event', 
                       'model_domain']

    forecast_format = f"|{'|'.join(forecast_fields)}|"

    openai_max_tokens = 30000

    def format(self):
        rec = vars(self)
        fmt = '|'.join([f"{x}: {rec[x]}" for x in self.forecast_fields])
        return '|' + fmt + '|'

    def over_openai_max(self):
        sep = self.format()
        return len(sep.split(' ')) > self.openai_max_tokens # Max limit for OpenAI

    def init_from_metaculus(self):
        self.question_details = get_question_details(self.question_id)
        self.today = datetime.now().strftime("%Y-%m-%d")   
        self.active_state = self.question_details["active_state"]
        self.title = self.question_details["title"]
        self.resolution_criteria = self.question_details["resolution_criteria"]
        self.background = self.question_details["description"]
        self.fine_print = self.question_details["fine_print"]
        self.resolution = self.question_details["resolution"]

    def init_from_db(self):
        print('init_from_db')
        conn = sqlite3.connect('q3ai.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ask_date, id, title, active_state, resolution, background, fine_print, resolution_criteria, json FROM ifp WHERE id = ?", (self.question_id,))
        (self.ask_date, self.question_id, self.title, self.active_state, \
         self.resolved, self.background, self.fine_print, self.resolution_criteria, self.question_details) = cursor.fetchone()
        conn.close()
        self.question_details = json.loads(self.question_details)

    def __init__(self, question_id):
        self.question_id = question_id
        self.event = ''
        self.model_domain = ''
        self.feedback = ''
        if row_exists(question_id):
            self.init_from_db()
        else:
            self.init_from_metaculus()

    def report(self):
        rpt = f"""
The future event is described by this question: [ {self.title} ]
The resolution criteria are: [ {self.resolution_criteria} ]
The background is: [ {self.background} ]"""
        if self.fine_print:
            rpt += f"""
The fine print is: [ {self.fine_print} ]"""
        return rpt

    def upload(self):
        post_question_prediction(self.question_id, self.forecast)
        post_question_comment(self.question_id, self.rationale)

    def insert(self, ask_date):
        rec = (ask_date, ifp.question_id, ifp.title, ifp.active_state, ifp.resolved,
               ifp.background, ifp.fine_print, ifp.resolution_criteria, json.dumps(ifp.question_details))
       
        # Connect to the SQLite database
        conn = sqlite3.connect('q3ai.db')  # Replace 'your_database.db' with your database name
        cursor = conn.cursor()

        # Insert a row into the ifp table
        cursor.execute('''
            INSERT INTO ifp (ask_date, id, title, active_state, resolved, background, fine_print, resolution_criteria, json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', rec)
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()

if __name__=="__main__":
    from history import history

    import sqlite3
    from tqdm import tqdm
    conn = sqlite3.connect('q3ai.db')
    cursor = conn.cursor()       
    for key in tqdm(history):
        dt = datetime.strptime(key, '%d%b%y')
        for qid in tqdm(history[key]):
            ifp = IFP(qid)