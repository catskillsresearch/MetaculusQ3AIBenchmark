class Agent:
    def __init__(self, system_role, llm):
        self.llm = llm(system_role)

    def chat(self, prompt):
        return self.llm.chat(prompt)