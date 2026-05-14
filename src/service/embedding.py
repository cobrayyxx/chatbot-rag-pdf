from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import torch


class Embedding:
    def __init__(self, embedding_model:str = "all-MiniLM-L6-v2"):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.embedding_model = SentenceTransformer(embedding_model, device=device)


    def get_embedding(self, text:str):
        chunks = self.chunk_pdf(text)
        embedding = self.embedding_model.encode(chunks, show_progress_bar=True)
        return embedding, chunks
   
    def chunk_pdf(self, text, chunk_size=700):
        chunks = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100, 
                                                       separators=["\n\n", "\n", ". "," ", ""])
        chunks = text_splitter.split_text(text)
        return chunks

if __name__ == "__main__":
    embedding = Embedding()
    text = "This is a sample text to test the embedding function.\n\n It will be split into chunks and then embedded using the SentenceTransformer model."
    embedding_result, chunks = embedding.get_embedding(text)
    print(embedding_result)
    print(embedding_result.shape)