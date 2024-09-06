from nn_graph.graph import *

# Replace with a valid file path to your JSON file
file_path = "C:/Users/gk332/Documents/Example2_TestNetwork.json"
graph = SimpleNNNetworkGraph(file_path, show_info=True)
graph.draw_graph()
