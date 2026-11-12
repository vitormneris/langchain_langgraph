from typing import Sequence
from pydantic import ValidationError
from rich import print
from langchain.tools import BaseTool, tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage

@tool
def multiply(a: float, b: float) -> float:
    """Multiply a * b and return the result
    
    Args:
        a: Float multiplicand
        b: Float multiplier
    
    Returns:
        The resulting float of the expression a * b
    """
    return a * b

system_message: BaseMessage = SystemMessage("""You are a helpful assistant. You have access to tools.
When the user asks for something, first look if you have a tool that solve that problem""")

human_message: BaseMessage = HumanMessage("Quanto é 3300 vezes 17700?")

messages: Sequence[BaseMessage] = [system_message, human_message]

llm = init_chat_model("ollama:llama3.2:3b")

tools: Sequence[BaseTool] = [ multiply ]
tools_by_name = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)

llm_response: AIMessage = llm_with_tools.invoke(messages)
messages = [*messages, llm_response]

if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls", None):
    call = llm_response.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]

    try:
        content = tools_by_name[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    messages = [*messages, tool_message]

    llm_response: AIMessage = llm_with_tools.invoke(messages)

print(llm_response.content)
