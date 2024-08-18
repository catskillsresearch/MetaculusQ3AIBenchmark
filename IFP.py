import re, requests, json, datetime
from config import config

AUTH_HEADERS = {"headers": {"Authorization": f"Token {config.METACULUS_TOKEN}"}}
API_BASE_URL = "https://www.metaculus.com/api2"
WARMUP_TOURNAMENT_ID = 3349
SUBMIT_PREDICTION = True

def find_number_before_percent(s):
    # Use a regular expression to find all numbers followed by a '%'
    matches = re.findall(r'(\d+)%', s)
    if matches:
        # Return the last number found before a '%'
        return int(matches[-1])
    else:
        # Return None if no number found
        return None

def post_question_comment(question_id, comment_text):
    """
    Post a comment on the question page as the bot user.
    """

    response = requests.post(
        f"{API_BASE_URL}/comments/",
        json={
            "comment_text": comment_text,
            "submit_type": "N",
            "include_latest_prediction": True,
            "question": question_id,
        },
        **AUTH_HEADERS,
    )
    response.raise_for_status()
    print("Comment posted for ", question_id)

def post_question_prediction(question_id, prediction_percentage):
    """
    Post a prediction value (between 1 and 100) on the question.
    """
    url = f"{API_BASE_URL}/questions/{question_id}/predict/"
    response = requests.post(
        url,
        json={"prediction": float(prediction_percentage) / 100},
        **AUTH_HEADERS,
    )
    response.raise_for_status()
    print("Prediction posted for ", question_id)


def get_question_details(question_id):
    """
    Get all details about a specific question.
    """
    url = f"{API_BASE_URL}/questions/{question_id}/"
    response = requests.get(
        url,
        **AUTH_HEADERS,
    )
    response.raise_for_status()
    return json.loads(response.content)

def list_questions(tournament_id=WARMUP_TOURNAMENT_ID, offset=0, count=1000):
    """
    List (all details) {count} questions from the {tournament_id}
    """
    url_qparams = {
        "limit": count,
        "offset": offset,
        "has_group": "false",
        "order_by": "-activity",
        "forecast_type": "binary",
        "project": tournament_id,
        "status": "open",
        "type": "forecast",
        "include_description": "true",
    }
    url = f"{API_BASE_URL}/questions/"
    response = requests.get(url, **AUTH_HEADERS, params=url_qparams)
    response.raise_for_status()
    data = json.loads(response.content)
    return data



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

    def record(self):
        return self.format()
        if self.over_openai_max(): 
            self.news = ' '.join(self.news.split(' ')[0:int(0.5*self.openai_max_tokens)])
        if self.over_openai_max(): 
            self.research = ' '.join(self.research.split(' ')[0:int(0.5*self.openai_max_tokens)])
        if self.over_openai_max(): 
            raise Exception('IFP record over OpenAI max')
        return self.format()

    def __init__(self, question_id):
        self.question_id = question_id
        self.question_details = get_question_details(self.question_id)
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")   
        self.title = self.question_details["title"]
        self.resolution_criteria = self.question_details["resolution_criteria"]
        self.background = self.question_details["description"]
        self.fine_print = self.question_details["fine_print"]
        self.event = ''
        self.model_domain = ''
        self.feedback = ''

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

if __name__=="__main__":
    qid = 26775
    ifp = IFP(qid)
    ifps = {qid: ifp}
    print(ifp.record())