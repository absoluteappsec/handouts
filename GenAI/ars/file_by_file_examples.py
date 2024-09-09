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
    glob="**/taskManager",
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

system_prompt_template = """
You are a helpful code review assistant who is proficient in both security as well as functional review. You will be provided source code of a web application and tasked with answering questions about it.

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



"""
prompt = ChatPromptTemplate.from_messages(
            [
                ("human", prompt_template),
            ]
)
"""

llm = Ollama(model="llama3", temperature=0.6)

response_array = []

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
    response = chain.invoke({
        "question" : "Analyze the provided code for any security flaws you find in it and produce a summary of that analysis.",
        "context" : code
    })
    response_array.append(response)
    """
    for chunk in chain.stream({
        "question" : "Analyze the provided code for any security flaws you find in it and produce a summary of that analysis.",
        "context" : code
        }):
        print(chunk, end="", flush=True)
    """

second_system_prompt_template = """
You are a helpful code review assistant. Summarize all of the analysis that has been performed on the code so far (summaries are provided via context). Inform the user of any high risk security flaws and where they are located in the source code.

<context>
{context}
</context>
"""


second_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", second_system_prompt_template),
                ("human", """<question>{second_question}</question>""")
            ]
)

second_chain = (
        { "context": RunnablePassthrough() , "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

for chunk in second_chain.stream({
        "second_question" : "Point out any critical risk issues in the code base and provide the filename of where the flaw is located.",
        "context" : response_array
        }):
        print(chunk, end="", flush=True)