import sys
from langchain.agents import Tool, AgentExecutor,  LLMSingleActionAgent, AgentType, AgentOutputParser, create_sql_agent, load_tools, initialize_agent
from langchain.prompts import BaseChatPromptTemplate
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import SerpAPIWrapper, LLMChain, SQLDatabaseChain, OpenAI, PromptTemplate
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain.sql_database import SQLDatabase
from langchain.llms import OpenAI
from langchain.llms.openai import OpenAI
import re
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

# Define which tools the agent can use to answer user queries
search = SerpAPIWrapper()
db = SQLDatabase.from_uri("sqlite:///C:/users/saget/Desktop/Hackathon/notebooks/Intakes.db")
toolkit = SQLDatabaseToolkit(llm=OpenAI(temperature=0), db=db)

# Tools
SQL_agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True
)


llm = ChatOpenAI(temperature=0.0)
math_llm = OpenAI(temperature=0.0)
human_tools = load_tools(
    ["human"], 
    llm=math_llm,
)

human_agent_chain = initialize_agent(
    human_tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Create our tools
tools = [
    Tool(
        name="SQL",
        func=SQL_agent_executor.run,
        description="Useful for adding, modifying, and retrieving information from databases using DML"
    ),
    Tool(
        name="Human",
        func=human_agent_chain.run,
        description="Useful for asking the humans personal information"
    ),
]

# Set up the base template
template = """You are a chatbot that is designed to do client intake at a law firm.
As a chatbot, you are having a conversation with the client in order to gather the requisite information from them to fill a row in the database.
Start by querying the database to find out what information you are looking for in order to fill a row in the Client table and the Incident table.
Ask the human questions based off the column names and then add the human's answers to the database.

YOU SHOULD NOT WRAP THE THOUGHT, ACTION, ACTION INPUT, OR TOOL NAMES IN BRACKETS!!

You have access to the following tools:
{tools}
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of {tool_names} (do not under any circumstance wrap these tool names in brackets)
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
Question: {input}
{agent_scratchpad}"""

# Set up a prompt template
class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = " or ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]
    
prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)

class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
    
output_parser = CustomOutputParser()

llm = ChatOpenAI(temperature=0)

# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

agent_executor.run("Fill out all of the information in the database for one client and one incident had by that user. Ask the human user for input any time you don't have information")