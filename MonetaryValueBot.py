# type: ignore
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

# Change the path after sqlite: to where you have Cases.db stored on your machine
my_db = SQLDatabase.from_uri("sqlite:///Cases.db")
toolkit = SQLDatabaseToolkit(db=my_db, llm=OpenAI(temperature=0))

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True
)

agent_executor.run("Based on the level of compensation stored in the database, estimate how much money could be won from a car accident case")