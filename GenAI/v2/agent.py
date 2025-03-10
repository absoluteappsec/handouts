from langchain.agents import create_react_agent
from langchain_aws import ChatBedrock
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
import git
import os
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Load Env Variables
from dotenv import load_dotenv
load_dotenv()

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about code"
    args_schema: Type[BaseModel] = SearchInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        # Repo details to clone
        repo_url = 'https://github.com/redpointsec/vtm.git'
        local_path = './repo'
        if os.path.isdir(local_path) and os.path.isdir(os.path.join(local_path, '.git')):
            print("\nDirectory already contains a git repository.")
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
        splitter = RecursiveCharacterTextSplitter.from_language(
              language=Language.PYTHON, 
              chunk_size=8000, 
            chunk_overlap=20
        )
        texts = splitter.split_documents(documents)
        embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1')
        db = FAISS.from_documents(texts, embeddings)
        val =  db.similarity_search(query)
        return val
        #return "LangChain"

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")



tools = [CustomSearchTool()]

llm = ChatBedrock(
    model_id='us.anthropic.claude-3-5-haiku-20241022-v1:0',
    model_kwargs={"temperature": 0.6},
)

instructions = """You are an agent designed to detect insecure direct object 
reference vulnerabilities. 

Insecure Direct Object Reference (IDOR) vulnerabilities occur when the application
retrieves a database record with user-supplied input as the record id without
proper authorization. This allows an attacker to access unauthorized records.

There are times where you will need to reference the application's code base
in order to analyze the authorization mechanisms applied to wherever the 
potential IDOR vulneability is occurring and verify if they properly scope 
or authorize the user for the record they are attempting to retrieve or update.
The reason for this is that you will want to ensure the authorization decorator's
functionality enforces that the user is allowed to retrieve of modify the 
database record.

You have access to a vector database which you can use to search for answers 
to questions about code. When looking up function names, ensure that it is 
an exact match to the function name requested. This is especially important 
because the wrong authorization function name could lead to a misunderstanding 
of the IDOR vulnerability.

Only use the output of your search to answer the question. 
You might know the answer without performing a search, but you should still 
run the search in order to get the answer.
If it does not seem like you can write code to answer the question, 
just return "I don't know" as the answer.

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(instructions)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

input = """
@login_required
@user_passes_test(can_create_project)
def update_user_active(request):
    user_id = request.GET.get('user_id')
    User.objects.filter(id=user_id).update(is_active=False)
"""

agent_executor.invoke({"input": input, "chat_history": ""})
