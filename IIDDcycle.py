import openai
from decouple import config

api_key = config('API_KEY')
openai.api_key = api_key


from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('/Users/markirwin/llama_index/examples/paul_graham_essay/data_input').load_data()
index = VectorStoreIndex.from_documents(documents)


query_engine = index.as_query_engine()

# Identify the goals
end_goal_question="What do you think are the goals the author was trying to achive?"
end_goal_response = query_engine.query(end_goal_question)

# Identify the key insights etc
information_question="To achive those goals, what information such as insights ,data ,principles ,examples etc do you think the author used ? "
information_response = query_engine.query(information_question)

# Identify the key issues
issues_question="What key questions or issues do you think the author asked himself to achive those goals based on the information he used ?"
issues_response = query_engine.query(issues_question)

# Identify the decisions he made
decision_question="Based on the key questions or issues he asked him self, what decisions or solutions did he come up with ? "
decision_response = query_engine.query(decision_question)

# Identify the actions he made
action_question="Based on the decisions he made, what actions did the author take ? "
action_response = query_engine.query(action_question)

# Synthesize
with open("/Users/markirwin/llama_index/examples/paul_graham_essay/data_output/paul_graham_output.txt", "w") as file:
    file.write(str(end_goal_response) + str(information_response) + str(issues_response) + str(decision_response) + str(action_response))
    
documents = SimpleDirectoryReader("/Users/markirwin/llama_index/examples/paul_graham_essay/data_output").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

synthesize_question="Output this text in a structered format with 5 parts. The first: On the goals the author had. Second: On the information the author used. Third: On the issues the author asked. Fourth: On the decisions the authos made. Fifth: On the actions the author took."
synthesize_response = query_engine.query(synthesize_question)

print(synthesize_response)

#response = query_engine.query(question)
#print(response)