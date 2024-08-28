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
        self.gpt = Claude
        self.qr = QuestionRelator(self.gpt)
        self.ask = AskNews()
        self.mdc = ModelDomainClassifier(self.gpt)
        self.ifps = ifps

        
    def fit(self):
        print('MODEL DOMAIN')
        for ifp in self.ifps.values():
            self.mdc.classify(ifp)

        print('CORRELATOR')
        try:
            self.rho
        except:
            self.rho = self.qr.relate(self.ifps)
            
        print('NEWS')
        self.news = {event: None for event in self.rho}
        for event, group in self.rho.items():
            if self.news[event] is None:
                print('ASKING')
                self.news[event] = self.ask.research(group)    

        print('RATES')
        self.rates = {event: None for event in self.rho}
        for event, group in self.rho.items():
            if self.rates[event] is None:
                self.ra = RateAnalyzer(self.gpt)
                self.rates[event] = self.ra.assess(group, self.news[event])
                print('RATES', event, self.rates)
            
        for event, group in self.rho.items():
            print('FORECASTING', event)
            self.sf = Superforecaster(self.gpt)
            self.sf.forecast(event, self.news[event], self.rates[event], group)
            critic = Critic(self.gpt)
            for ifp in group:
                print("REFINING", ifp.id)
                for i in range(self.max_tries):
                    print("Pass", i, "of", self.max_tries, "on", ifp.id)
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
            print(ifp.id, ifp.title)
            print("Forecast", ifp.forecast)
            print("Rationale", ifp.rationale, '\n')

    def upload(self):
        for ifp in self.ifps.values():
            ifp.upload()

if __name__=="__main__":
    test_day = '01AUG24'
    ifps = {id: IFP(id) for id in history[test_day]}