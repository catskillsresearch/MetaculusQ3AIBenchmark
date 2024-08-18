class LLM:
    def __init__(self, system_role):
        self.system_role = system_role
        self.messages = [{"role": "system", "content": system_role}]
        self.cache = {}

    def chat(self, query):
        if query in self.cache:
            return self.cache[query]
        else:
            self.messages.append({"role": "user", "content": query})
            text = self.message()
            self.messages.append({"role": "assistant", "content": text})
            self.cache[query] = text
            return text