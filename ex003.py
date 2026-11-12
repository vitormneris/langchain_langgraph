from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph, add_messages

from rich import print

def reducer(a, b):
    print(f"> reducer {a=} {b=}")
    return add_messages(a, b)

# Definir o estado
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], reducer]

# Criando os nodes
def call_llm(state: AgentState) -> AgentState:
    return { 'messages': [ AIMessage("Olá, tudo bem e você?") ] }

# Criando o builder
builder = StateGraph(
    state_schema=AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState
)

# Adicionado os nodes
builder.add_node("call_llm", call_llm)

# Definir as adges
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

graph = builder.compile()

if __name__ == '__main__':
    response = graph.invoke( { 'messages': [ HumanMessage("Olá, tudo bem?") ] } )
    print(response)

