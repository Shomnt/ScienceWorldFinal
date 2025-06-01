import asyncio

from fastapi import FastAPI
from neo4j import GraphDatabase

app = FastAPI()

# Подключение к Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "strongpassword8810"))

@app.post("/create_area/")
async def create_area(name: str):
    def create_node(tx, name):
        tx.run("CREATE (:Area {name: $name})", name=name)

    with driver.session() as session:
        session.execute_write(create_node, name)

    return {"message": "Node created"}

@app.post("/create_connection/")
async def connect_area(name1: str, name2: str, weight: float):
    def create_relationship(tx, name1, name2, weight):
        query = """
        MATCH (a:Area {name: $name1}), (b:Area {name: $name2})
        CREATE (a)-[:KNOWS {weight: $weight}]->(b)
        """
        tx.run(query, name1=name1, name2=name2, weight=weight)

    with driver.session() as session:
        session.execute_write(create_relationship, name1, name2, weight)

    return {"message": f"{name1} now knows {name2}"}

areas = dict()
with open("../../../../ScienceWorld_v2/graph-service/create/ScienceList.txt", "r") as f:
    for line in f:
        f, s = line.split(":")
        f, s = f.strip(), s.strip()
        if areas.get(f, None) is None:
            areas[f] = list()
        areas[f].append(s)

async def create_db(handle_connections: tuple[list, list, list] = None) -> None:
    for first_layer, second_layers in areas.items():
        await create_area(first_layer)
        for second_layer in second_layers:
            await create_area(second_layer)
            await connect_area(second_layer, first_layer, 0.77)
            await connect_area(first_layer, second_layer, 1.0)
    if handle_connections is not None:
        if len(handle_connections[0]) != len(handle_connections[1]) or len(handle_connections[0]) != len(handle_connections[2]):
            raise Exception("The length of all lists must be equal to the number of connections")
        for i in range(len(handle_connections[0])):
            if handle_connections[2][i] == 0.0:
                continue
            await connect_area(handle_connections[0][i], handle_connections[1][i], handle_connections[2][i])

areas_list = list(areas.keys())
from_list = []
for i in range(len(areas_list)):
    for j in range(len(areas_list[i+1:])):
        from_list.append(areas_list[i])
for i in range(len(areas_list)-1, -1, -1):
    for j in range(len(areas_list[:i])):
        from_list.append(areas_list[i])
print(len(from_list))
to_list = []
for i in range(len(areas_list)):
    to_list.extend(areas_list[i+1:])
for i in range(len(areas_list)-1, -1, -1):
    to_list.extend(areas_list[:i])
print(len(to_list))

weight_list = ["0.01","0.73","0.1","0","0","0.01","0","0","0","0.62","0","0","0","0","0","0","0.01","0.01","0","0","0","0","0",
               "0.6","0.4","0","0","0","0","0","0","0.07","0.3","0","0.05","0","0","0.05","0","0","0","0","0","0.08","0",
               "0.7","0","0","0","0","0","0","0.07","0","0","0","0","0","0.77","0","0","0","0","0","0","0",
               "0","0","0","0","0.2","0","0.1","0","0","0","0","0.01","0.4","0","0.6","0","0","0","0","0.2",
               "0.01","0","0","0.25","0","0","0","0","0","0","0.7","0","0","0.2","0","0","0","0","0.2",
               "0.01","0.01","0","0.7","0","0.01","0.01","0.01","0.1","0","0.01","0.01","0","0","0.01","0","0.01","0",
               "0.01","0.01","0.01","0","0.05","0.25","0","0","0.4","0","0.25","0","0.4","0.15","0","0.25","0",
               "0","0.01","0","0.15","0.15","0.15","0.15","0","0","0.15","0","0.01","0.15","0.48","0.15","0",
               "0","0.001","0","0","0","0","0.7","0","0","0.7","0","0","0","0","0.7",
               "0","0.15","0","0","0.25","0","0","0.25","0","0.15","0.15","0.15","0.15","0",
               "0","0","0","0","0","0","0","0.02","0","0","0","0","0",
               "0.02","0.1","0.1","0","0","0.25","0","0.08","0.01","0.25","0.25","0",
               "0","0","0","0","0.3","0","0.61","0.01","0.01","0.18","0",
               "0.34","0","0","0.15","0","0.01","0.01","0","0.01","0",
               "0","0","0.07","0","0.01","0.1","0.01","0.01","0",
               "0","0","0.7","0","0","0","0","0.7",
               "0","0","0","0.7","0","0","0",
               "0","0.25","0.1","0.7","0.25","0",
               "0","0","0","0","0.7",
               "0.7","0.15","0.7","0",
               "0.57","0.65","0",
               "0.68","0",
               "0"
]
weight_list = list(map(float, weight_list))
weight_list = weight_list + weight_list[::-1]

if __name__ == "__main__":
    asyncio.run(create_db((from_list, to_list, weight_list)))