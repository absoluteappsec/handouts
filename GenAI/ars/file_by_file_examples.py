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
    chunk_size=8000, 
    chunk_overlap=20
)

texts = splitter.split_documents(documents)

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

llm = Ollama(model="llama3", temperature=0.6)

for text in texts:
    # Pull the actual code in string format
    code = text.page_content
    # Retrieve filename for reference
    filename = text.metadata.get("source", "unknown")
    # Create a chain of operations to run the code through
    chain = (
        { "context": RunnablePassthrough() , "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # This is an optional addition to stream the output in chunks
    # for a chat-like experience
    title = f"\n\nAnalyzing code from {filename}"
    print(title)
    print("=" * len(title))
    for chunk in chain.stream({
        "question" : "Analyze the provided code for any security flaws you find in it and produce a summary of that analysis.",
        "context" : code
        }):
        print(chunk, end="", flush=True)