from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

# Change the path after sqlite: to where you have Cases.db stored on your machine
db = SQLDatabase.from_uri("sqlite:///C:/users/saget/Desktop/Hackathon/notebooks/Cases.db")
toolkit = SQLDatabaseToolkit(db)

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True
)

agent_executor.run("Based on the level of compensation stored in the database, estimate how much money could be recovered from a case where the plaintiff was injured by a staircase collapsing and suffered permanent paralysis from the waist down")