import os
import git
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

# Load Env Variables
from dotenv import load_dotenv
load_dotenv()

# For BedRock
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock

# For Ollama
#from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_community.llms import Ollama

repo_url = 'https://github.com/redpointsec/vtm.git'
local_path = './repo'

if os.path.isdir(local_path) and os.path.isdir(os.path.join(local_path, '.git')):
    print("Directory already contains a git repository.")
else:
    try:
        repo = git.Repo.clone_from(repo_url, local_path)
        print(f"Repository cloned into: {local_path}")
    except Exception as e:
        print(f"An error occurred while cloning the repository: {e}")

docs = []
for dirpath, dirnames, filenames in os.walk(local_path):
    for file in filenames:
        extension = Path(file).suffix 
        if (
            extension == '.py' or
            file == 'requirements.txt'
            ):
            try:
                print(f"Processing {file}")
                loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                docs.extend(loader.load_and_split())
            except Exception as e:
                pass

# UNCOMMENT FOR LLAMA
#embeddings = HuggingFaceEmbeddings()

embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1')

splitter = RecursiveCharacterTextSplitter(
    chunk_size=8000,
    chunk_overlap=20
)

texts = splitter.split_documents(docs)

system_prompt_template = """
You are a helpful code review assistant who is proficient
in both security as well as functional review. You will be
provided source code of a web application and tasked with
answering questions about it.

<context>
{context}
</context>
"""

# CORRECT/FORMAL WAY TO PERFORM PROMPTING
prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_template),
                ("human", """<question>{question}</question>""")
            ]
)

# UNCOMMENT FOR OLLAMA/LLAMA
#llm = Ollama(model="llama3.1", temperature=0.6)

llm = ChatBedrock(
    model_id='anthropic.claude-3-haiku-20240307-v1:0',
    model_kwargs={"temperature": 0.6},
)

db = FAISS.from_documents(texts, embeddings)

retriever = db.as_retriever(
    search_type="mmr", # Also test "similarity"
    search_kwargs={"k": 8},
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# This is an optional addition to stream the output in chunks
# for a chat-like experience
for chunk in chain.stream(
    """Analyze the codebase comprehensively and provide a detailed application profile with the following information:
    
    ## 1. Application Behavior Analysis
    
    - Business Purpose: What is the primary function or business goal of the application?
    - Target Audience: Who is the application built for (internal users, external customers)?
    - Data Handling: What types of data does the application store, process, or transmit?
      - Identify data types handled
      - Note any sensitive data present
      - Describe data storage approaches
    - User Roles: What different types of roles or user permissions exist within the system?
      - Describe role types and hierarchies
      - Explain permission scopes
      - Identify access control patterns
    
    ## 2. Language & Framework Analysis
    
    - Programming Language: What primary language(s) are used, including versions?
      - List language features utilized
      - Note any implementation details
    - Development Framework: What main framework(s) is the application built on?
      - Include framework name and version
      - List key framework components used
      - Describe framework configuration details
    - Architecture Pattern: What architectural patterns are implemented (MVC, etc.)?
      - Explain how the pattern is implemented
      - Identify key architectural components
    - Build & Deployment: How is the application built and deployed?
      - Note build tools and processes
      - Describe deployment configuration
      - Explain environment management
    
    ## 3. Components & Libraries Analysis
    
    List all significant libraries by name, purpose, and version for these categories:
    - Security Components:
      - Authentication libraries
      - Authorization components
      - Encryption/cryptography libraries
      - Other security-focused dependencies
    - Database Components:
      - ORMs and query builders
      - Database drivers and connectors
      - Migration and schema management tools
    - Frontend Components:
      - JavaScript frameworks and libraries
      - CSS frameworks and preprocessors
      - Asset management tools
    - API & Integration Components:
      - API clients
      - Third-party service SDKs
      - Data format libraries (JSON, XML, etc.)
    - Other Notable Dependencies:
      - Utility libraries
      - Development and testing tools
      - Specialized domain-specific libraries
    
    ## 4. Datastores & Templating Analysis
    
    - Datastores: What databases and storage mechanisms are used?
      - Database types and versions
      - Caching mechanisms
      - File storage approaches
      - Database configuration details
    - Database Schema: How is data structured?
      - Key tables/collections and their purpose
      - Data relationships
      - Schema management approach
    - Data Access Patterns: How does the application interact with data?
      - Query patterns
      - Data access layers
      - Transaction handling
    - Templating Engines: How does the application generate output?
      - Template engine(s) used
      - Template organization
      - View rendering process
    - User Interface Construction: How is data presented to users?
      - View components
      - UI frameworks
      - Client-side rendering approaches
    """
    ):
    print(chunk, end="", flush=True)
