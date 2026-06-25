from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


class Embeddings:

    def __init__(self, chunks):
        self.chunks = chunks

        self.embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

    def embed(self):

        texts = [
            chunk.page_content
            for chunk in self.chunks
        ]

        vectors = self.embedding_model.embed_documents(texts)

        return list(zip(self.chunks, vectors))