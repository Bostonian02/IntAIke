# Imports
from langchain import LLMMathChain, LLMChain, SQLDatabaseChain
from langchain.agents import create_sql_agent, ZeroShotAgent, Tool, AgentExecutor
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
# import wolfram alpha shit for the wolfram alpha tool
# from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from dotenv import load_dotenv
import sqlite3

def get_monetary_value():
    # Load API Keys
    load_dotenv()

    db = SQLDatabase.from_uri("sqlite:///Cases.db")
    toolkit = SQLDatabaseToolkit(llm=OpenAI(temperature=0), db=db)
    # Tools
    # wolfram = WolframAlphaAPIWrapper()
    SQL_agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0),
        toolkit=toolkit,
        verbose=True
    )
    # Create our tools
    tools = [
        Tool(
            name="SQL",
            func=SQL_agent_executor.run,
            description="Useful for retrieving information from databases"
        ),
        # Tool(
        #     name="Math",
        #     func=wolfram.run,
        #     description="Useful for when you need to do math operations"
        # ),
    ]

    # Prefix and suffix
    prefix="Answer the following questions as best you can. You have access to the following tools:"
    suffix="""Your goal is to give a rough estimate of how much money a case could make based on the data in the database.
    Your estimate does not have to be a perfect average. Your estimate should take into account the severity of the incident based on its description.
    If the incident was worse relative to the example descriptions in the database, the amount of money that could be won should be larger.
    Remember to give either a range or a single value as your final answer. Begin!
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

    # Grab the category from the SQL database
    # connection = sqlite3.connect('Intakes.db')
    # cursor = connection.cursor()
    # cursor.execute('SELECT CASE_TYPE FROM Incidents')
    # results = cursor.fetchall()

    # cursor.close()
    # connection.close()

    prompt = "Based on the amount of money won stored in the database, estimate how much money could be won from a case where the type is Car Accident"
    # Run the agent
    return agent_executor.run(prompt)