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
    model_id='us.anthropic.claude-3-5-haiku-20241022-v1:0',
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
    """Tell me the following information about the code base I am providing you:
     - Purpose of the vtm application
     - Web technologies used in the vtm application
     - Templating language used in the vtm application
     - Database used in the vtm application
     - Authentication mechanisms used in the vtm application
     - Authorization mechanisms used in the vtm application


     List libraries by their name, purpose, and version that are
    used in the vtm application for the following categories:
        - Security
        - Testing
        - Documentation
        - Build
        - Database
        - Authentication / Authorization
        - HTML Templating (ex: pug, handlebars)
        - CSS Frameworks (ex: bootstrap, tailwind)
        - widgets / UI components
    """
    ):
    print(chunk, end="", flush=True)
