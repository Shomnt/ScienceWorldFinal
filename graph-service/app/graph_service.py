from neo4j import AsyncSession

from .edge_schema import EdgeGetIn, EdgeGetOut


async def get_path_weight(db: AsyncSession, user_area: str, area: str) -> float:
    result = await db.run("""
            MATCH (start:Area {name: $fr}), (end:Area {name: $to}),
                  path = shortestPath((start)-[:KNOWS*0..5]->(end))
            RETURN [rel IN relationships(path) | properties(rel)] AS edge_props_list
        """, fr=user_area, to=area)
    record = await result.single()
    edge_props  = record["edge_props_list"] if record else []
    if len(edge_props) == 0:
        return 0
    answer = 1
    for elem in edge_props :
        answer *= elem.get("weight", 1)
    return answer



async def get_value(db: AsyncSession, data:EdgeGetIn) -> EdgeGetOut:
    rating = 0
    for node in data.user_area_list:
        for node2 in data.article_area_list:
            weight = await get_path_weight(db, node, node2)
            rating += (weight * data.user_rating)
    return EdgeGetOut(
        addition_rating=rating,
    )
