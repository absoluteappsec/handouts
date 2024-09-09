import os
import git
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

loader = GenericLoader.from_filesystem(
    local_path,
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON),
)

documents = loader.load()
embeddings = HuggingFaceEmbeddings()

splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, 
    chunk_size=16000, 
    chunk_overlap=20
)

texts = splitter.split_documents(documents)
print(texts)

db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever(
    search_type="mmr", # Also test "similarity"
    search_kwargs={"k": 8},
)

prompt_template = """
You are a helpful code review assistant who is proficient in both security as well as functional review. You will be provided source code of a web application and tasked with answering questions about it.

<context>
{context}
</context>

<question>
{question}
</question>
"""

prompt = ChatPromptTemplate.from_messages(
            [
                ("human", prompt_template),
            ]
)


# CORRECT/FORMAL WAY TO PERFORM PROMPTING
#prompt = ChatPromptTemplate.from_messages(
#            [
#                ("system", system_prompt_template),
#                ("human", """<question>{question}</question>""")
#            ]
#)


llm = Ollama(model="llama3", temperature=0.6)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

"""
THE FOLLOWING IS A LIST OF EXAMPLE QUESTIONS TO ASK THE MODEL. UNCOMMENT TO USE.
"""

question = "Which Django authorization decorators are used in this application code base and where are they located?"
#question = "The following is a Django application code base. Tell me everything you can about the application that might be important to know as a security professional."

for chunk in chain.stream(question):
    print(chunk, end="", flush=True)