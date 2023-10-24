# Basic setup
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="/Users/markirwin/llama_index/.env")

# #Pinecone setup
# import pinecone
# api_key = os.environ["PINECONE_API_KEY"]
# environment = os.environ["PINECONE_ENVIRONMENT"]
# pinecone.init(api_key=api_key, environment=environment)

# index_name = "llamaindex-rag-fs"

# pinecone.create_index(
#     index_name, dimension=1536, metric="euclidean", pod_type="p1"
# )
# pinecone_index = pinecone.Index(index_name)

# #Create PineconeVectorStore
# from llama_index.vector_stores import PineconeVectorStore
# vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
