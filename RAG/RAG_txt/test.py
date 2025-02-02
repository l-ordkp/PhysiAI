from neo4j import GraphDatabase
import os

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+ssc://957c71ca.databases.neo4j.io"
AUTH = (os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD') )

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()