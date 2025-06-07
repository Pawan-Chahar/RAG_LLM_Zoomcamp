# Module 1: Introduction
## 1.1 Introduction

* LLM
* RAG
* RAG architecture
* Course Outcome


## 1.2 Preparing the Enviroment

Installing libraries
Alternative: installing anaconda or miniconda

pip install tqdm notebook==7.1.2 openai elasticsearch==8.13.0 pandas scikit-learn ipywidgets



## 1.3 Retrieval 

Note: as of now, you can install minsearch with pip:

pip install minsearch

* We will use the search engine we build in the build-your-own-search-engine workshop: minsearch
* Indexing the documents
* Peforming the search

## 1.4 Generation

Video

* Invoking OpenAI API
* Building the prompt
* Getting the answer


## 1.5 Cleaned RAG flow

Video

* Cleaning the code we wrote so far
* Making it modular


## 1.6 Searching with ElasticSearch

* Run ElasticSearch with Docker
* Index the documents
* Replace the MinSearch with ElasticSearch

Running ElasticSearch:

'''
docker run -it \
    --rm \
    --name elasticsearch \
    -m 4GB \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
'''

If the previous command doesn't work (i.e. you see "error pulling image configuration"), try to run ElasticSearch directly from Docker Hub:

'''
docker run -it \
    --rm \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    elasticsearch:8.4.3
    '''

Index settings:
'''
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} 
        }
    }
}
'''

Query:
'''
{
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
'''

We use "type": "best_fields". You can read more about different types of multi_match search in elastic-search.md.

## 1.7 Homework

More information here.

Extra materials
If you're curious to know how the code for parsing the FAQ works, check this video
Open-Source LLMs (optional)
It's also possible to run LLMs locally. For that, we can use Ollama. Check these videos from LLM Zoomcamp 2024 if you're interested in learning more about it:

Ollama - Running LLMs on a CPU
Ollama & Phi3 + Elastic in Docker-Compose
UI for RAG
