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

def get_trial_prob(case_type):
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
    suffix="""Your goal is to give a rough estimate of the probability of a case going to trial based on the data in the database.
    Start by making a list of related cases and whether they have gone to trial. Make the list by getting information  from the database column Trial.
    The column Trial is Boolean, represented by 0 as false and 1 as true. You can represent those values as percentages with 0 meaning 0% and 1 meaning 100%. Add all of the 1s and 0s together, and then divide by the total number of items in the list you created in order to get the final percentage value.

    Remember to give a percentage as a string representing the likelyhood a case goes to trial as your final answer.
    If you encounter an error, make up a percentage and give that as a string as your final answer.
    Begin!
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

    prompt = "Based on the cases that go to trial in the database, estimate the probability of a case going to trial if its type is " + case_type
    # Run the agent
    return agent_executor.run(prompt)