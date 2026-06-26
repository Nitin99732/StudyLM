from chromadb import PersistentClient


class VectorStore:

    def __init__(
        self,
        collection_name: str = "studylm",
        db_path: str = "./chroma_db",
    ):

        self.client = PersistentClient(path=db_path)

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(self, embedded_chunks):

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for index, (chunk, embedding) in enumerate(
            embedded_chunks,
            start=1
        ):

            ids.append(str(index))

            documents.append(
                chunk.page_content
            )

            embeddings.append(
                embedding
            )

            metadatas.append(
                chunk.metadata
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"{len(ids)} chunks stored successfully.")