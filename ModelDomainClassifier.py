from Agent import Agent

class ModelDomainClassifier(Agent):
    def __init__(self, llm):
        self.system_role = f"""
A question about an event is formatted as |id|question|criteria|background|fineprint|.
You will report the model domain of the question, one of

Rate over time
Weather prediction
State executive action
Election outcome
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
"""
        super().__init__(self.system_role, llm)

    def classify(self, ifp):
        prompt = f"|{ifp.question_id}|{ifp.title}|{ifp.resolution_criteria}|{ifp.background}|{ifp.fine_print}|"
        self.R = self.chat(prompt)
        ifp.model_domain = self.R
        print(ifp.question_id, ifp.title)
        print(self.R)

if __name__=="__main__":
    from MetaAI import MetaAI
    mdc = ModelDomainClassifier(MetaAI)
    for ifp in ifps.values():
        mdc.classify(ifp)