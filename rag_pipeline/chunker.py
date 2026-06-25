from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

class Chunker:

    def __init__(
          self, 
          text : str,
          chunk_size: int = 512,
          chunk_overlap: int = 100
    ):
        self.text = text
        
        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3")
            ]
        )

        self.recursive_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="text-embedding-3-small",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    
    def split(self):

      headers_doc = self.markdown_splitter.split_text(self.text)

      final_chunks = []

      parent_id = 1

      for doc in headers_doc:
          
        if len(doc.page_content) <= self.recursive_splitter._chunk_size:
           
          doc.metadata.update(
              {
                 "parent_chunk_id" : parent_id,
                 "chunk_number" : 1,
              }
          )

          final_chunks.append(doc)

        else:
           
          recursive_doc = self.recursive_splitter.create_documents([doc.page_content])

          for index, chunk in enumerate(recursive_doc, start=1):
             
            chunk.metadata.update(doc.metadata)

            chunk.metadata.update(
               {
                  "parent_chunk_id": parent_id,
                  "chunk_number": index
               }
            )

            final_chunks.append(chunk)

        parent_id += 1
      
      return final_chunks


obj = Chunker("")
docs = obj.split()

for doc in docs:
    print(doc.metadata)
    print(doc.page_content)