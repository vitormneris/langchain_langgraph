from langgraph.graph import StateGraph
from typing import Annotated, TypedDict

# Criando o estado
class State(TypedDict):
    nodes_path: Annotated[list[str], lambda a, b: a + b]

# Criando os nodes
def node_a(state: State) -> State:
    output_state: State = { "nodes_path": ["A"] }
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state

def node_b(state: State) -> State:
    output_state: State = { "nodes_path": ["B"] }
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state

# Definir o builder do grafo
builder = StateGraph(State)

# Definir os nós/nodes
builder.add_node("A", node_a)
builder.add_node("B", node_b)

# Definir as arestas/edges
builder.add_edge("__start__", "A")
builder.add_edge("A", "B")
builder.add_edge("B", "__end__")

# Compilar o grafo
graph = builder.compile()

# Pegar o resultado
response = graph.invoke({ "nodes_path": [] })

# Imprimir resultado
print()
print(response)
print()
