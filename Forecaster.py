from IFP import IFP
from QuestionRelator import QuestionRelator
from AskNews import AskNews
from ModelDomainClassifier import ModelDomainClassifier
from RateAnalyzer import RateAnalyzer
from Superforecaster import Superforecaster
from Critic import Critic
from MetacGPT import MetacGPT
from Claude import Claude

# Starting from https://colab.research.google.com/drive/1_Il5h2Ed4zFa6Z3bROVCE68LZcSi4wHX?usp=sharing

class Forecaster:
    
    def __init__(self, ifps):
        self.max_tries = 4
        self.qr = QuestionRelator(MetacGPT)
        self.ask = AskNews()
        self.mdc = ModelDomainClassifier(MetacGPT)
        self.ifps = ifps
        
    def fit(self):
        print('MODEL DOMAIN')
        for ifp in self.ifps.values():
            self.mdc.classify(ifp)
        print()  
        print('CORRELATOR')
        self.rho = self.qr.relate(self.ifps)
        print('FORECASTER')
        for event, group in self.rho.items():
            print('FORECASTING EVENT', event)
            self.news = self.ask.research(group)   
            print('NEWS')
            print(self.news)
            self.ra = RateAnalyzer(Claude)
            self.rates = self.ra.assess(group, self.news)
            print('RATES', self.rates)
            self.sf = Superforecaster(MetacGPT)
            self.sf.forecast(event, self.news, self.rates, group)
            critic = Critic(MetacGPT)
            for ifp in group:
                print("REFINING", ifp.question_id)
                for i in range(self.max_tries):
                    print("Pass", i, "of", self.max_tries, "on", ifp.question_id)
                    if 'concur' in ifp.feedback:
                        print("concur 1")
                        break
                    critic.feedback(ifp)
                    if 'concur' in ifp.feedback:
                        print("concur 2")
                        break
                    self.sf.reassess(ifp)
                print("===============================================")

    def report(self):
        for ifp in self.ifps.values():
            print(ifp.question_id, ifp.title)
            print("Forecast", ifp.forecast)
            print("Rationale", ifp.rationale, '\n')

    def upload(self):
        for ifp in self.ifps.values():
            ifp.upload()

if __name__=="__main__":
    test_day = '01AUG24'
    ifps = {id: IFP(id) for id in history[test_day]}