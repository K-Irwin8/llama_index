import openai
from decouple import config

api_key = config('API_KEY')
openai.api_key = api_key


from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('/Users/markirwin/llama_index/examples/paul_graham_essay/data').load_data()
index = VectorStoreIndex.from_documents(documents)


query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)