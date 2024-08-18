from Agent import Agent
from IFP import IFP

class Superforecaster(Agent):
    def __init__(self, llm):
        self.system_role = f"""
You are a superforecaster.  
You assign a probability to questions about events.
Questions are given as GROUP|group_description followed by NEWS|group_news followed by RATES|group_rates 
followed by the questions in the group formatted QUESTIONS followed by, for each question, {IFP.forecast_format}.
Questions which are about the same event should be assigned consistent probabilities.
Reply to questions with |ASSESSMENT|id|ZZ|rationale| where ZZ is an integer probability from 1 to 99 and rationale is your reasoning for the forecast.
Separate each question with '^^^'.
Do not add any additional headings or group labels or other formatting.
After your initial forecast you may receive feedback of form |CRITIC|id|feedback|.
Reply to each feedback with |id|ZZ|rationale| where ZZ is an integer probability from 1 to 99 and 
and rationale is a revised assessment which may be adjusted from a prior assessment due the feedback unless the feedback is "I concur".
"""
        super().__init__(self.system_role, llm)

    def forecast(self, event, news, rates, group):
        ifpstr = '\n'.join([ifp.record() for ifp in group])
        prompt = f"GROUP|{event}\nNEWS|{news}\nRATES|{rates}\nQUESTIONS\n{ifpstr}"
        self.F0 = self.chat(prompt)
        self.F1 = [x.strip().replace('\n', '') for x in self.F0.split('^^^')]
        self.F2 = [x.split('|') for x in self.F1] 
        self.F3 = [[x for x in y if x] for y in self.F2]
        self.F4 = [(int(id),int(forecast),rationale) for _, id, forecast, rationale in self.F3]
        self.ifps = {ifp.question_id: ifp for ifp in group}
        for id, forecast, rationale in self.F4:
            self.ifps[id].forecast = forecast
            self.ifps[id].rationale = rationale
            print(id, forecast, rationale)

    def reassess(self, ifp):
        prompt = f"|CRITIC|{ifp.question_id}|{ifp.feedback}|"
        self.R0 = self.chat(prompt)
        id,fcst,rationale = [x for x in self.R0.strip().split('|') if x]
        id = int(id)
        fcst = int(fcst)
        self.ifps[id].forecast = fcst
        self.ifps[id].rationale = rationale
        print(id, fcst, rationale)

if __name__=="__main__":
    from MetaAI import MetaAI
    sf = Superforecaster(MetaAI)
    event = '2024 Grand Chess Tour'
    group = qr.topic_groups[event]
    sf.forecast(event, news, r, group)