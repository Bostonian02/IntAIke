# CURRENT ISSUE:
#
# IT'S DOING THE FUN THING WHERE IT ADDS BRACKETS AROUND THE NAME OF THE TOOL IT WANTS TO USE
# FIX THAT AND IT WORKS MAYBE POSSIBLY I THINK I HOPE

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import create_sql_agent, load_tools, initialize_agent, ZeroShotAgent, Tool, AgentType, AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

template = """This is a conversation between a human and a bot:

{chat_history}

Write a summary of the conversation for {input}:
"""

prompt = PromptTemplate(
    input_variables=["input", "chat_history"], 
    template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=memory)
summry_chain = LLMChain(
    llm=OpenAI(), 
    prompt=prompt, 
    verbose=True, 
    memory=readonlymemory, # use the read-only memory to prevent the tool from modifying the memory
)

# Creating shit to make tools? idk man i made this 16 hours ago idrk how it works anymore
db = SQLDatabase.from_uri("sqlite:///C:/users/saget/Desktop/Hackathon/notebooks/Intakes.db")
toolkit = SQLDatabaseToolkit(llm=OpenAI(temperature=0), db=db)
SQL_agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    memory=readonlymemory,
)
llm = ChatOpenAI(temperature=0.0)
human_tools = load_tools(
    ["human"], 
    llm=llm,
    memory=readonlymemory,
)
# human_agent_chain = initialize_agent(
#     human_tools,
#     llm,
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     memory=readonlymemory,
# )

# Create our tools
tools = [
    Tool(
        name="SQL",
        func=SQL_agent_executor.run,
        description="Useful for retrieving data from the database and adding data to the database"
    ),
    Tool(
        name="Human",
        func=human_tools.run,
        description="Useful for asking the user questions in order to gather the information you need"
    ),
    Tool(
        name = "Summary",
        func=summry_chain.run,
        description="Useful for when you summarize a conversation. The input to this tool should be a string, representing who will read this summary."
    )
]

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""

suffix = """Begin!
UNDER ABOSLUTELY NO CIRCUMSTANCES ARE YOU TO EVER WRAP THE NAME OF A TOOL IN BRACKETS.
WRAPPING THE NAME OF A TOOL YOU PLAN TO USE IN BRACKETS WILL CAUSE IT TO FAIL."

{chat_history}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools, 
    prefix=prefix, 
    suffix=suffix, 
    input_variables=["input", "chat_history", "agent_scratchpad"]
)

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

agent_chain.run(input="Ask the user for a description of the incident that led them to seek legal help.")
agent_chain.run(input="You may ask a few clarifying questions to gather more detail at your discretion.")
agent_chain.run(input="Send a summary of the description you gathered to the description field of the Incidents table in the database.")
