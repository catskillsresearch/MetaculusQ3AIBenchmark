from Agent import Agent
import datetime

class RateAnalyzer(Agent):
    def __init__(self, llm):
        self.today = str(datetime.datetime.now())[0:10]
        self.system_role = f"""
A group of events are given, formatted as "GROUP" followed by a group of questions separated by carriage returns, followed by "NEWS" followed by news on the topic.
Today's date is {self.today }.
If the question is about a level that changes at some rate over time, you will report 
1. today's date, 
2. the end date of the question, 
3. the time in days D from today to end date, 
4. the daily rate of change R of the quantity,
5. today's value V of the quantity,
6. the change in value dV of the quantity = D * r,
7. the final value of the quantity F = V + dV.  Give your best estimate.
Otherwise if the question is about the date that an event will occur, you will report
1. today's date, 
2. the end (measurement) date of the question, 
3. the time in days D from today to end date, 
4. the specific date at which the event is most likely to occur, without reference to the end date of the question
5. whether the likely event date is before, or on or after the question end date

Provide only one type of answer, not both.
"""
        super().__init__(self.system_role, llm)

    def assess(self, group, news):
        titles = '\n'.join([ifp.title.strip() for ifp in group])
        self.q = f'GROUP\n{titles}\nNEWS\n{news}'
        self.rates = self.chat(self.q)
        return self.rates

if __name__=="__main__":
    from MetaAI import MetaAI
    try:
        group
    except:
        group = [IFP(id) for id in [26771, 26772, 26773, 26774]]

    rates = RateAnalyzer(MetaAI)
    r = rates.assess(group, news)
    print(r)