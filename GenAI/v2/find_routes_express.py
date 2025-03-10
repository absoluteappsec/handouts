import os
import git
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
# UNCOMMENT FOR OLLAMA
#from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_community.llms import Ollama
# For BedRock
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load Env Variables
from dotenv import load_dotenv
load_dotenv()

repo_url = 'https://github.com/absoluteappsec/skea_node.git'
local_path = './repo'

if os.path.isdir(local_path) and os.path.isdir(os.path.join(local_path, '.git')):
    print("Directory already contains a git repository.")
else:
    try:
        repo = git.Repo.clone_from(repo_url, local_path)
        print(f"Repository cloned into: {local_path}")
    except Exception as e:
        print(f"An error occurred while cloning the repository: {e}")


loader = GenericLoader.from_filesystem(
    local_path,
    glob="**/*",
    suffixes=[".js"],
    parser=LanguageParser(language=Language.JS),
    show_progress=True
)   

documents = loader.load()

# UNCOMMENT FOR OLLAMA
#embeddings = HuggingFaceEmbeddings()

embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1')

splitter = RecursiveCharacterTextSplitter.from_language(language=Language.JS, 
    chunk_size=8000, 
    chunk_overlap=20
)
texts = splitter.split_documents(documents)

db = FAISS.from_documents(texts, embeddings)

system_prompt_template = """
You are a helpful code assistant who is given acess to a
code base stored in vector format. You will be asked questions about that code.
Please provide helpful and accurate responses to the best of your ability.

</context>
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
retriever = db.as_retriever(
    search_type="mmr", # Also test "similarity"
    search_kwargs={"k": 8},
)

# UNCOMMENT FOR OLLAMA/LLAMA
#llm = Ollama(model="llama3.1", temperature=0.6)

llm = ChatBedrock(
    model_id='us.anthropic.claude-3-5-haiku-20241022-v1:0',
    model_kwargs={"temperature": 0.6},
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

question = """
Please provide me with a summary of where the HTTP
routes are defined in this code base. Please print them out in a format
similar to how rake routes would display them with the following collumns:

VERB | URI | FILE | LINE NUMBERS

Example:

GET | / | app.js | 10-20
"""

# This is an optional addition to stream the output in chunks
# for a chat-like experience
for chunk in chain.stream(question):
    print(chunk, end="", flush=True)

