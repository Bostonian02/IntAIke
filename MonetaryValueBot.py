# Imports
from langchain import LLMMathChain, LLMChain, SQLDatabaseChain
from langchain.agents import create_sql_agent, ZeroShotAgent, Tool, AgentExecutor
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

# Tools
my_db = SQLDatabase.from_uri("sqlite:///Cases.db")
db_chain = SQLDatabaseChain(llm=OpenAI(temperature=0), database=my_db, verbose=True)
llm_math_chain = LLMMathChain(llm=OpenAI(temperature=0), verbose=True)

# Create our tools
tools = [
    Tool(
        name="SQL",
        func=db_chain.run,
        description="Useful for retrieving information from databases"
    ),
    Tool(
        name="Math",
        func=llm_math_chain.run,
        description="Useful for when you need to do math operations"
    ),
]

# Prefix and suffix
prefix="Answer the following questions as best you can. You have access to the following tools:"
suffix="""Begin!

Question: {input}
{agent_scratchpad}"""

# Create the prompt
prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "agent_scratchpad"]
)

# Create the chain and agent
llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

# Run the agent
agent_executor.run("Based on the level of compensation stored in the database, estimate how much money could be won from a car accident case")