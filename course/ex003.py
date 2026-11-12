from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph, add_messages

from rich import print

llm = init_chat_model("ollama:llama3.2:3b")

# Definir o estado
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Criando os nodes
def call_llm(state: AgentState) -> AgentState:
    result_llm = llm.invoke(state['messages'])
    return { 'messages': [result_llm] }

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
    while True:
        user_input = input("Insira a mensagem (q para sair): ")
        if user_input in ['q', 'quit']:
            break
        human_message = HumanMessage(user_input)
        response = graph.invoke( { 'messages': [ human_message ] } )
        print(f'AI: {response['messages'][-1].content}')
