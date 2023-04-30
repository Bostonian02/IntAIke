# Imports
from langchain import OpenAI, LLMMathChain, SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# Setup
llm = ChatOpenAI(temperature=0)
llm1 = OpenAI(temperature=0)
wikipedia = WikipediaAPIWrapper()
db = SQLDatabase.from_uri("sqlite:///Cases.db")
db_chain = SQLDatabaseChain(llm=llm1, database=db, verbose=True)
tools = [
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Useful for looking up information on virtually any topic"
    ),
    Tool(
        name="Cases DB",
        func=db_chain.run,
        description="Useful for when you need information about cases. Input should be in the form of a question containing full context. Do not use quotes for a SQL query"
    )
]

mrkl = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

mrkl.run("How much money could I win from a car accident case?")