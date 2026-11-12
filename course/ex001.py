from dataclasses import dataclass
from langgraph.graph import END, START, StateGraph
from typing import Annotated
import operator

# Criando o estado
@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]

# Criando os nodes
def node_a(state: State) -> State:
    output_state: State = State(nodes_path=["A"])
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state

def node_b(state: State) -> State:
    output_state: State = State(nodes_path=["B"])
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state

# Definir o builder do grafo
builder = StateGraph(State)

# Definir os nós/nodes
builder.add_node("A", node_a)
builder.add_node("B", node_b)

# Definir as arestas/edges
builder.add_edge(START, "A")
builder.add_edge("A", "B")
builder.add_edge("B", END)

# Compilar o grafo
graph = builder.compile()

# Pegar o resultado
response = graph.invoke(State(nodes_path = []))

# Imprimir resultado
print()
print(f"{response=}")
print()
