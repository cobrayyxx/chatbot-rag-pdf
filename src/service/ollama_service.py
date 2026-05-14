from langchain_ollama import ChatOllama



class OllamaService:
    def __init__(self, model:str = "qwen2.5:0.5b", temperature: int = 0):
        self.llm = ChatOllama(
                        model= model,
                        temperature= temperature,
                    )

    def generate_response(self, query: str) -> str:
        messages = [
                (
                    "system",
                    "You are a helpful chatbot assistant that will answer questions based on the provided context. If you don't know the answer, say you don't know.",
                ),
                ("human", f"{query}"),
            ]
        response = self.llm.invoke(messages)
        return response.content
    
    def create_prompt(self, query: str, context: str) -> str:
        prompt = f"""
        Answer the question based on the following context. If you don't know the answer, say you don't know.
        Context: {context}
        Question: {query}
        """
        return prompt

if __name__ == "__main__":
    ollama_service = OllamaService()
    prompt = "What is the capital of France?"
    response = ollama_service.generate_response(prompt)
    print(response)