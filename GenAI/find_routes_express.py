import os
import git
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


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
)   

documents = loader.load()
embeddings = HuggingFaceEmbeddings()

splitter = RecursiveCharacterTextSplitter.from_language(language=Language.JS, 
    chunk_size=8000, 
    chunk_overlap=20
)
texts = splitter.split_documents(documents)


db = FAISS.from_documents(texts, embeddings)

template = """
<s>[INST] <<SYS>>
Answer the question below based on the provided context.

{context}
<</SYS>>

{question} [/INST]
"""

prompt = PromptTemplate.from_template(template)
retriever = db.as_retriever(
    search_type="mmr", # Also test "similarity"
    search_kwargs={"k": 8},
)

llm = Ollama(model="llama3", temperature=0.6)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

response = chain.invoke("Where are HTTP routes defined in this codebase?")
print(response)

# This is an optional addition to stream the output in chunks
# for a chat-like experience
for chunk in chain.stream("Where are HTTP routes defined in this codebase?"):
    print(chunk, end="", flush=True)
