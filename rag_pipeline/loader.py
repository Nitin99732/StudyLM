from llama_cloud import LlamaCloud
from dotenv import load_dotenv

load_dotenv()

class DocumentParser:

    def __init__(self, file_path):
        self.client = LlamaCloud() # Reads LLAMA_CLOUD_API_KEY automatically
        self.file_path = file_path

        self.file = self.client.files.create(
            file=self.file_path,
            purpose="parse"
        )

    
    def parse(self):

        return self.client.parsing.parse(
            file_id=self.file.id,
            tier="agentic",
            version="latest",

            processing_options={
                "specialized_chart_parsing": "agentic",

                "aggressive_table_extraction": True,

                "cost_optimizer": {
                    "enable": True
                }
            },

            output_options={
                "markdown": {
                    "tables": {
                        "merge_continued_tables": True
                    }
                }
            },

            expand=[
                "markdown",
                "metadata",
                "items"
            ]
        )
    

loader = DocumentParser("")
result = loader.parse()

