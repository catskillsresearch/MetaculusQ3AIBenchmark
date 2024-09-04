from Agent import Agent

class ModelDomainClassifier(Agent):
    def __init__(self, llm):
        self.system_role = f"""
A question about an event is formatted as |id|question|criteria|background|fineprint|.
You will report the model domain of the question, one of

Aerospace technology
Rate over time
Weather prediction
State executive action
Corporate action
Stock price
Rate change
Market cap
Election outcome
Entertainment
Geopolitics
Sports performance
Military conflict
Civil unrest
Dated product announcement
Market price
Macroeconomics
Epidemic
Disease
Drug discovery
Medical device
Crime
Leadership change
AI performance
Astronomy
Astrophysics
Other

The report should consist of the model domain as listed above ONLY, with no additional text or delimiters.
"""
        super().__init__(self.system_role, llm)

    def classify(self, ifp):
        prompt = f"|{ifp.id}|{ifp.title}|{ifp.resolution_criteria}|{ifp.background}|{ifp.fine_print}|"
        self.R = self.chat(prompt)
        ifp.model_domain = self.R
        print(ifp.id, ifp.title)
        print(self.R)
        return self.R

if __name__=="__main__":
    from MetacGPT import MetacGPT
    mdc = ModelDomainClassifier(MetacGPT)
    for ifp in ifps.values():
        mdc.classify(ifp)