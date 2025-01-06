from py2neo import Graph, Node, Relationship
import PyPDF2
import pandas as pd

# Connect to Neo4j Database
def connect_to_neo4j(uri, username, password):
    graph = Graph(uri, auth=(username, password))
    return graph

# Extract Text and Tables from PDF
def extract_text_and_tables(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text_data = []
    for page in pdf_reader.pages:
        text_data.append(page.extract_text())

    return text_data

# Store Text and Tables in Neo4j
def store_in_neo4j(graph, text_data):
    for idx, text in enumerate(text_data):
        node = Node("Page", page_number=idx + 1, content=text)
        graph.create(node)
