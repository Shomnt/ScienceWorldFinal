from neo4j import AsyncGraphDatabase

driver = AsyncGraphDatabase.driver("bolt://graph-service:7687", auth=("neo4j", "strongpassword123"))

async def get_db():
    async with driver.session() as session:
        yield session
