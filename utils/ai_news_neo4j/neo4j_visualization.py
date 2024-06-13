from py2neo import Graph
import networkx as nx
import matplotlib.pyplot as plt

def visualize_neo4j_database(uri, user, password):
    graph = Graph(uri, auth=(user, password))
    query = """
        MATCH (a:Article)-[r:MENTIONS]->(e:Entity)
        RETURN a, r, e
    """
    data = graph.run(query).data()
    G = nx.DiGraph()
    for record in data:
        article = record['a']
        entity = record['e']
        relationship = record['r']
        G.add_node(article['id'], label=article['title'], color='blue')
        G.add_node(entity['name'], label=entity['name'], color='red')
        G.add_edge(article['id'], entity['name'], weight=relationship['count'])
    pos = nx.spring_layout(G)
    node_colors = [node[1]['color'] for node in G.nodes(data=True)]
    node_labels = {node[0]: node[1]['label'] for node in G.nodes(data=True)}
    nx.draw_networkx_nodes(G, pos, node_color=node_colors)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    visualize_neo4j_database("bolt://localhost:7687", "neo4j", "6EBsJd-oiSo0aV65CsplXKBe-BIkPMXoEi2DWbo1-bM")