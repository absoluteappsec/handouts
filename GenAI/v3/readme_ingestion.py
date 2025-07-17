import requests
from langchain_core.documents import Document
#from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock

# Load Env Variables
from dotenv import load_dotenv
load_dotenv()

# UNCOMMENT FOR OLLAMA
#llm = Ollama(model="llama3", temperature=0.6)
llm = ChatBedrock(
    model_id='us.anthropic.claude-3-haiku-20240307-v1:0',
    model_kwargs={"temperature": 0.6},
)

question = """
QUESTION
========
{question}

CONTEXT
=======
{context}
"""
prompt = ChatPromptTemplate.from_template(template=question)
README_URL = 'https://raw.githubusercontent.com/juice-shop/juice-shop/master/README.md'
response = requests.get(README_URL)
if response.status_code == 200:
    readme_content = response.content
    doc = Document(
        page_content=readme_content, 
        metadata={"source": "README.md"}
    )
    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    # Stream the output in chunks for a chat-like experience
    for chunk in chain.stream({
        "question":"""
        You are an application security professional analyzing a software project. You've been provided with the README file from the project. Extract and organize the following security-relevant information:

        ## 1. Application Overview
        - Core purpose and functionality of the application
        - Target users/audience
        - Primary technologies, frameworks, and programming languages used
        - Deployment models (cloud, on-premise, container-based, etc.)

        ## 2. Security Considerations
        - Any mentioned security features or security-related functionality
        - Authentication and authorization mechanisms
        - Data protection features or encryption approaches
        - Security-related configuration options
        - API security information

        ## 3. Security Risk Indicators
        - Known vulnerabilities or security issues mentioned
        - Security warnings or disclaimers
        - Whether it's a deliberately vulnerable application (like DVWA, Juice Shop)
        - References to security testing tools or processes

        ## 4. Dependencies & Components
        - Major third-party libraries and dependencies
        - External services or APIs integrated
        - Database technologies used
        - Client-side frameworks/libraries

        ## 5. Application Architecture
        - Component structure or architecture diagrams described
        - Data flow information
        - Communication protocols mentioned
        - Network services or exposed ports

        ## 6. Documentation & Resources
        - Links to additional documentation that might contain security information
        - Security-related documentation mentioned
        - Security contacts or responsible disclosure policies

        Format your findings as a structured security briefing. If certain information is not available in the README, explicitly note its absence as this itself may be a security consideration. Be thorough but concise.
        """, 
        "context": doc
    }):
        print(chunk, end="", flush=True)
