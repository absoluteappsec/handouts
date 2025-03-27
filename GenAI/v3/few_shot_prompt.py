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
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Load Env Variables
from dotenv import load_dotenv
load_dotenv()

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
    show_progress=True
)   

documents = loader.load()
#embeddings = HuggingFaceEmbeddings()
embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1')

splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, 
    chunk_size=8000, 
    chunk_overlap=20
)
texts = splitter.split_documents(documents)


db = FAISS.from_documents(texts, embeddings)

system_prompt_template = """
You are a helpful secure code review assistant who is given acess to a
code base stored in vector format. You will be asked questions about that code.
Please provide helpful and accurate responses to the best of your ability.

</context>
{context}
</context>

<background>
 Django's ORM methods automatically handle SQL escaping
 in order to prevent SQL Injection attacks. Unsafe SQL
 queries can only be run with the following functions:
 `.raw()`, `.execute()`, `.extra()`.
</background>
"""


retriever = db.as_retriever(
    search_type="mmr", # Also test "similarity"
    search_kwargs={"k": 8},
)

#llm = Ollama(model="llama3", temperature=0.6)
llm = ChatBedrock(
    model_id='us.anthropic.claude-3-5-haiku-20241022-v1:0',
    model_kwargs={"temperature": 0.6},
)


# This is an optional addition to stream the output in chunks
# for a chat-like experience
question = """
Identify everywhere in the Django application code base that contains
SQL Injection vulnerablities. Only tell me about the code that is vulnerable
to SQL Injection. Don't mention code that is not vulnerable to SQL Injection.
"""


prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_template),
                ("human", """<question>{question}</question>""")
            ]
)

examples = [

    {
        "context": """
            def get_users(username):
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE username = '%s'" % username)
                return cursor.fetchall()
        """,
        "question": "Identify everywhere in the Django application code base that contains SQL Injection vulnerablities.",
        "answer": "This code is vulnerable to SQL Injection because it takes the username (user input) and directly concatenates it into the SQL query."
    },
    {
        "context": """
            def get_users(username):
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE username = %s", [username])
                return cursor.fetchall()
        """,
        "question": "Identify everywhere in the Django application code base that contains SQL Injection vulnerablities.",
        "answer": """
            Although the code uses the `cursor.execute()` method, it is using
            parameterized queries, therefore it is not
            vulnerable to SQL Injection.
        """
    },
    {
        "context":"""
            if re.match('.*?(rm|sudo|wget|curl|su|shred) .*',ip,re.I):
                data = "Nice try on the dangerous commands, but no"
            else:
                cmd = "ping -c 5 %s" % ip
                data = subprocess.getoutput(cmd)
        """,
        "question":"Identify everywhere in the Django application code base that contains SQL Injection vulnerablities.",
        "answer": """
            This code is not vulnerable to SQL Injection because it is command injection so I will not mention it.
        """
    },
    {
        "context": """
            ssn = forms.CharField(max_length=11, required=False)
        """,
        "question": "Identify everywhere in the Django application code base that contains SQL Injection vulnerablities.",
        "answer": """
            This code is not vulnerable to SQL Injection because it is a form field definition.
        """
    }
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{question}\n{context}"),
        ("ai", "{answer}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        few_shot_prompt,
        ("human", """<question>{question}</question>""")
    ]
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | final_prompt
    | llm
    | StrOutputParser()
)

for chunk in chain.stream(question):
    print(chunk, end="", flush=True)
