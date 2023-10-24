# Basic setup
import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex
load_dotenv(dotenv_path="/Users/markirwin/llama_index/.env")

#Pinecone setup
import pinecone
api_key = os.environ["PINECONE_API_KEY"]
environment = os.environ["PINECONE_ENVIRONMENT"]
pinecone.init(api_key=api_key, environment=environment)

index_name = "llamaindex-rag-fs"

# pinecone.create_index(
#     index_name, dimension=1536, metric="euclidean", pod_type="p1"
# )
pinecone_index = pinecone.Index(index_name)

#Create PineconeVectorStore
from llama_index.vector_stores import PineconeVectorStore
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)






#print("Hello Kai !")

# Load data
import fitz
file_path = "./data/llama2.pdf"
doc = fitz.open(file_path)


#Use a Text Splitter to Split Documents
    #やっぱ sentance splitter では質が悪いね
from llama_index.text_splitter import SentenceSplitter

text_splitter = SentenceSplitter(
    chunk_size=1024,
    # separator=" ",
)

text_chunks = []
# maintain relationship with source doc index, to help inject doc metadata in (3)
doc_idxs = []
for doc_idx, page in enumerate(doc):
    page_text = page.get_text("text")
    cur_text_chunks = text_splitter.split_text(page_text)
    text_chunks.extend(cur_text_chunks)
    doc_idxs.extend([doc_idx] * len(cur_text_chunks))

#Manually Construct Nodes from Text Chunks
    # なるほど！ you split the text, and make them into nodes ! We make them into a "textnode" object
    #This essentially replicates logic in our SimpleNodeParser.
    
from llama_index.schema import TextNode

nodes = []
for idx, text_chunk in enumerate(text_chunks):
    node = TextNode(
        text=text_chunk,
    )
    src_doc_idx = doc_idxs[idx]
    src_page = doc[src_doc_idx]
    nodes.append(node)
    
    

# [Optional] 4. Extract Metadata from each Node 
#     こういうMetadataExtractor,QuestionsAnsweredExtractor,TitleExtractor 等のものを自分で customize する必要があるってことだね
    
# from llama_index.node_parser.extractors import (
#     MetadataExtractor,
#     QuestionsAnsweredExtractor,
#     TitleExtractor,
# )
# from llama_index.llms import OpenAI

# llm = OpenAI(model="gpt-3.5-turbo")

# metadata_extractor = MetadataExtractor(
#     extractors=[
#         TitleExtractor(nodes=5, llm=llm),
#         QuestionsAnsweredExtractor(questions=3, llm=llm),
#     ],
#     in_place=False,
# )

# nodes = metadata_extractor.process_nodes(nodes)
    
# print(nodes[0].metadata)
# # print a sample node
# print(nodes[0].get_content(metadata_mode="all"))


# Generate Embeddings for each Node
from llama_index.embeddings import OpenAIEmbedding

embed_model = OpenAIEmbedding()

for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding
    
    
# Load Nodes into a Vector Store
vector_store.add(nodes)


from llama_index import VectorStoreIndex
from llama_index.storage import StorageContext

index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
query_str = "Can you tell me about the key concepts for safety finetuning"
response = query_engine.query(query_str)
print(str(response))