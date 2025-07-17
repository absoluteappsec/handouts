from langchain.agents import create_react_agent
from langchain_aws import ChatBedrock
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from pydantic import BaseModel, Field
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
    query: str = Field(description="Provide the exact function name you wish to have us search in a vector database for")

class CustomSearchTool(BaseTool):
    name: str = "custom_search"
    description: str = "This tool will allow you to provide a function or class name and get back the definition of that code"
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
    model_id='us.anthropic.claude-3-haiku-20240307-v1:0',
    model_kwargs={"temperature": 0.6},
)

instructions = """You are an agent designed to detect insecure direct object 
reference vulnerabilities. 

Insecure Direct Object Reference (IDOR) vulnerabilities occur when the application
retrieves or modifies a database record using user-supplied input as the record id without
proper authorization checks to ensure the user has permission to access or modify that specific record.

When analyzing code for IDOR vulnerabilities, look for the following patterns:

1. User-supplied IDs directly used in database operations (via URL parameters, GET/POST data, etc.)
2. Missing or insufficient authorization checks on those specific records
3. Use of decorators like that only check if a user is logged in but don't check if they have permission to access the specific resource
4. Lack of ownership verification between the logged-in user and the resource being accessed

Follow this analysis process:

1. Identify where the code gets an ID from user input (URL, GET/POST parameters)
2. Check if there are proper authorization checks specifically verifying this user has permission to access this exact resource
3. Determine if any permission decorators are scoped only to user roles but don't check resource ownership
4. Look for direct database operations using the user-supplied ID without verification

Authorization should involve:
- Checking that the user is authenticated
- AND checking that the user has appropriate permissions for their role
- AND checking that the user has permission to access the specific resource identified by the ID

Missing any of these, especially the last one, is likely an IDOR vulnerability.

You have access to a vector database which you can use to search for function definitions to understand how authorization is implemented. Look for functions like:

1. The specific view function being analyzed
2. Any permission check functions used in decorators (like can_create_project)
3. Any functions that check ownership between users and resources

When you identify an IDOR vulnerability, clearly explain:
1. Where the vulnerability is located
2. How the code takes user input without proper authorization
3. How an attacker could exploit it
4. What specific check is missing to fix it

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

New input: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(instructions)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

input = """
# This function deactivates any user account when provided a user_id
@login_required
@user_passes_test(can_create_project)
def update_user_active(request):
    # Get user_id from URL parameter
    user_id = request.GET.get('user_id')
    # Directly update the user without checking if the logged-in user has permission
    # to modify this specific user_id
    User.objects.filter(id=user_id).update(is_active=False)
    return HttpResponse('User deactivated successfully')
"""

agent_executor.invoke({"input": input})
