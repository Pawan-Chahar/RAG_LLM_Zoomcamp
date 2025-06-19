import streamlit as st
import time
from loguru import logger
from elasticsearch import Elasticsearch
import json 
import os 
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


client = Groq(api_key = os.environ.get('GROQ_API_KEY'))

logger.info(f'{client}')

es_client = Elasticsearch(
    ['http://localhost:9200'],
    headers={
        "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
        "Content-Type": "application/json"
    }  
)

def elastic_search(query, index_name = "course-questions"):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    logger.info(f'elastic_search : {result_docs}') 
    return result_docs
    

def build_prompt(query, search_results):
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()

    logger.info(f'build_prompt  : {prompt}')
    return prompt
    

def llm(prompt):
    response = client.chat.completions.create(
        model='llama3-70b-8192',
        messages=[{"role": "user", "content": prompt}]
    )
    
    logger.info(f'response : {response.choices[0].message.content}')
    return response.choices[0].message.content


def rag(query):
    search_results = elastic_search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer


def main():
    st.title("RAG Function Invocation")

    user_input = st.text_input("Enter your input:")

    if st.button("Ask"):
        with st.spinner('Processing...'):
            output = rag(user_input)
            st.success("Completed!")
            st.write(output)

if __name__ == "__main__":
    main()