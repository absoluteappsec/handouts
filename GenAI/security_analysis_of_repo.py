import os
import git
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Repo URL to download
repo_url = 'https://github.com/redpointsec/vtm.git'
# Local path we store the code in
local_path = './repo'

# Make sure we don't clone the repo if it already exists and clone if it doesn't
if os.path.isdir(local_path) and os.path.isdir(os.path.join(local_path, '.git')):
    print("Directory already contains a git repository.\n")
else:
    try:
        repo = git.Repo.clone_from(repo_url, local_path)
        print(f"Repository cloned into: {local_path}")
    except Exception as e:
        print(f"An error occurred while cloning the repository: {e}")

# Load the file system into a loader object
loader = GenericLoader.from_filesystem(
    local_path,
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON),
)   

# Create documents out of the loaded files
documents = loader.load()

# Create object to split code into chunks recursivley maintaining the language code format
splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, 
    chunk_size=8000, 
    chunk_overlap=20
)

# Split the documnets into chunks
texts = splitter.split_documents(documents)

# Create a prompt template using CodeLLaMa's LLM tags (INST, SYS, s)
template = """
<s>[INST] <<SYS>>
Answer the question below based on the provided code.

{code}
<</SYS>>

{question} [/INST]
"""

# Turn the template into prompt template object
prompt = PromptTemplate.from_template(template)

# Instantiate the CodeLLaMa LLM model
llm = Ollama(model="codellama", temperature=0.6)

# Iterate through each chunk of code and prompt the LLM model to analyze it
for text in texts:
    # Pull the actual code in string format
    code = text.page_content
    # Retrieve filename for reference
    filename = text.metadata.get("source", "unknown")
    # Create a chain of operations to run the code through
    chain = (
        { "code": RunnablePassthrough() , "question": RunnablePassthrough()}
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
        "code" : code
        }):
        print(chunk, end="", flush=True)
