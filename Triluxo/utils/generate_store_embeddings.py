from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
#resolving the nltk error 
import nltk




import os
from dotenv import load_dotenv
load_dotenv()
index_name = "triluxo"

api_key = os.getenv("PINECONE")

class Embeding_DB:
    def __init__(self, index_name = "triluxo", api_key = api_key, filename = "output.txt", chunk_data = ""):
        self.index_name = index_name
        self.api_key = api_key
        self.filename = filename
        self.chunk_data = chunk_data
        

    def Embed_Save(self):
        """
        returns the retirver object
        """
        #initizing the pinecone clinet
        pc = Pinecone(api_key=self.api_key)

        try:
            # Retrieve the list of existing indexes
            existing_indexes = pc.list_indexes()
            print(f"Existing indexes: {existing_indexes}")

            if self.index_name not in existing_indexes:
                # Create the index if it doesn't exist
                pc.create_index(
                    name=self.index_name,
                    dimension=384,  # Dimension of your dense model
                    metric='dotproduct',  # Metric for similarity search
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
                print(f"Index '{self.index_name}' created successfully.")
            else:
                print(f"Index '{self.index_name}' already exists.")

        except Exception as e:
            if e.status == 409:
                # Handle the case where the index already exists
                print(f"Index '{index_name}' already exists. Proceeding to use it.")
            else:
                # Handle other potential exceptions
                print(f"An error occurred while creating the index: {e}")
        
        index = pc.Index(index_name)


        embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
        os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
        bm25_encoder = BM25Encoder().default() #defining the default encoder i.e .default()

        # data = self.file_to_list()
        # chunk = self.chunk_list(data, 50, 20)
        # chunk_data = ["".join(chunk[i]) for i in range(len(chunk))]

        # Download the punkt tokenizer model
        nltk.download('punkt_tab')

        #tfidf values  on these sentences
        bm25_encoder.fit(self.chunk_data)

        #store the values as json files
        bm25_encoder.dump("bm25_values.json")

        #loading the encoder object
        bm25_loaded = BM25Encoder().load("bm25_values.json")

        retriver = PineconeHybridSearchRetriever(embeddings=embeddings, sparse_encoder=bm25_encoder, index=index)
        retriver.add_texts(self.chunk_data)

        return retriver



    # Function to convert text file to Python list
    def file_to_list(self):
        with open(self.filename, 'r') as file:
            # Read the file content
            content = file.read()
            # Split the content by lines and return as a list
            lines_list = content.splitlines()  # Each line will be a separate item in the list
        return lines_list
    
    def chunk_list(self,data, chunk_size, overlap):
        """
        Split a list into chunks with specified chunk size and overlap length.

        :param data: List to be chunked
        :param chunk_size: Size of each chunk
        :param overlap: Overlap length between consecutive chunks
        :return: List of chunks
        """
        if chunk_size <= overlap:
            raise ValueError("Chunk size must be greater than overlap length.")
        
        # Create chunks with overlap
        chunks = []
        for i in range(0, len(data), chunk_size - overlap):
            chunk = data[i:i + chunk_size]
            chunks.append(chunk)
            if len(chunk) < chunk_size:
                break  # Stop if the last chunk is smaller than the chunk size
        return chunks
    
