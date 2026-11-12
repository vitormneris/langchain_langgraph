from dataclasses import dataclass
from langgraph.graph import END, START, StateGraph
from typing import Annotated, Literal
import operator

# Criando o estado
@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 100

# Criando os nodes
def node_a(state: State) -> State:
    output_state: State = State(nodes_path=["A"], current_number=state.current_number)
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state

def node_b(state: State) -> State:
    output_state: State = State(nodes_path=["B"], current_number=state.current_number)
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state

def node_c(state: State) -> State:
    output_state: State = State(nodes_path=["C"], current_number=state.current_number)
    print("> node_c", f"{state=}", f"{output_state=}")
    return output_state

# Criando a condicional
def the_conditional(state: State) -> Literal["B", "C"]:
    if state.current_number >= 50:
        return "B"
    return "C"

# Definir o builder do grafo
builder = StateGraph(State)

# Definir os nós/nodes
builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

# Definir as arestas/edges
builder.add_edge(START, "A")
builder.add_conditional_edges("A", the_conditional, ["B", "C"])
builder.add_edge("B", END)
builder.add_edge("C", END)

# Compilar o grafo
graph = builder.compile()

# Pegar o resultado
response = graph.invoke(State(nodes_path = []))

# Imprimir resultado
print()
print(f"{response=}")
print()
