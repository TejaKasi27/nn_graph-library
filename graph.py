import json
import math
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import RegularPolygon

class SimpleNNNetworkGraph:
    """
    A class for creating and visualizing neural network graphs based on JSON model descriptions.

    This class reads a JSON file containing a neural network model description,
    creates a graph representation of the network, and provides methods to visualize it.
    """

    def __init__(self, file_path, base_node_size=0.5, edge_width=2, mutation_scale=15, show_info=False, fig_size=(14, 10), file_format='png'):
        """
        Initialize the SimpleNNNetworkGraph object.

        Args:
            file_path (str): Path to the JSON file containing the network model.
            base_node_size (float): Base size for nodes in the graph. Default is 0.5.
            edge_width (int): Width of edges in the graph. Default is 2.
            mutation_scale (int): Scale factor for arrow mutations. Default is 15.
            show_info (bool): Whether to show additional info on edges. Default is False.
            fig_size (tuple): Size of the figure for plotting. Default is (14, 10).
            file_format (str): Format for saving the graph image. Default is 'png'.
        """
        self.file_path = file_path
        self.base_node_size = base_node_size
        self.edge_width = edge_width
        self.mutation_scale = mutation_scale
        self.show_info = show_info
        self.fig_size = fig_size
        self.file_format = file_format
        self.network_data = self._load_network_data()
        self.G = self._create_graph()

    def _convert_color(self, color_str):
        """
        Convert a color string to RGBA format.

        Args:
            color_str (str): Color string in format "r g b" or "r g b a".

        Returns:
            tuple: RGBA color tuple.
        """
        color_tuple = tuple(map(float, color_str.split()))
        return to_rgba(color_tuple)

    def _load_network_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error at position {e.pos}: {e.msg}")
            print(f"Problematic content: {content[max(0, e.pos-20):e.pos+20]}")
            raise
        


    def _create_graph(self):
        """
        Create a NetworkX graph representation of the neural network.

        Returns:
            networkx.DiGraph: Directed graph representation of the network.
        """
        network_id = list(self.network_data.keys())[0]
        network = self.network_data[network_id]
        G = nx.DiGraph()

        node_shapes = {
        'excitatory': '^',
        'inhibitory': 'o',
        'generic': 's',
        'input': 'h'
        }

        # Add population nodes with default shape
        for pop_id, pop in network['populations'].items():
            G.add_node(pop_id, color=self._convert_color(pop['properties']['color']),
                   shape=node_shapes['generic'], size=pop['size'])
    
        # Initialize synapse types tracking for nodes
        node_synapse_types = {node: set() for node in G.nodes}

        # Add input source nodes and edges
        if 'inputs' in network and network['inputs']:
            for input_id, input_info in network['inputs'].items():
                G.add_node(input_id, color=self._convert_color("1 1 0"), 
                       shape=node_shapes['input'], size=2)  # Yellow for input sources
                # There is no information about size in inputs section
                # Add edges for inputs
                self._add_input_edge(G, input_id, input_info, network['input_sources'])
                node_synapse_types[input_id] = 'dummy'  # Mark input node

            # Update node shapes based on their synapse types
            self._update_node_shapes(G, node_synapse_types, node_shapes)

        # Add edges and determine node types based on projections
        for proj in network['projections'].values():
            self._add_projection(G, proj, node_synapse_types, node_shapes, network)

        return G


    def _add_projection(self, G, proj, node_synapse_types, node_shapes, network):
        """
        Add a projection (edge) to the graph and update node synapse types.

        Args:
            G (networkx.DiGraph): The graph to update.
            proj (dict): Projection information.
            node_synapse_types (dict): Dictionary to track node synapse types.
            node_shapes (dict): Dictionary of node shapes.
        """
        pre_pop = proj['presynaptic']
        post_pop = proj['postsynaptic']
        synapse_type = proj.get('synapse', 'generic')
        style = 'dashed' if proj.get('random_connectivity', {}).get('probability', 1) < 1 else 'solid'
        edge_attrs = self._get_edge_attributes(synapse_type, proj,style, network)
        node_synapse_types[pre_pop].add(edge_attrs['synapse_category'])

        if proj.get('directionality') == 'bidirectional':
            G.add_edge(pre_pop, post_pop, **edge_attrs)
            G.add_edge(post_pop, pre_pop, **edge_attrs)
        else:
            G.add_edge(pre_pop, post_pop, **edge_attrs)

    def _get_edge_attributes(self, synapse_type, proj, style, network):
        """
        Get edge attributes based on synapse type and projection properties.

        Args:
            synapse_type (str): Type of synapse.
            proj (dict): Projection information.

        Returns:
            dict: Edge attributes.
        """
        if synapse_type == 'ampaSyn':
            return {
                'synapse': proj['synapse'],
                'style': style,
                'arrowstyle': '-|>',
                'color': 'blue',
                'info': self._format_edge_info(proj),
                'synapse_category': 'excitatory'
            }
        elif synapse_type == 'gabaSyn':
            return {
                'synapse': proj['synapse'],
                'style': style,
                'arrowstyle': None,
                'color': 'red',
                'info': self._format_edge_info(proj),
                'synapse_category': 'inhibitory'
            }
        else:
            
            return {
                'synapse': proj['synapse'],
                'style': style,
                'arrowstyle': '->',
                'color': self._convert_color(network['populations'][proj['presynaptic']]['properties']['color']),
                'info': self._format_edge_info(proj),
                'synapse_category': 'generic'
            }


    def _format_edge_info(self, proj):
        """
        Format edge information string.

        Args:
            proj (dict): Projection information.

        Returns:
            str: Formatted edge information.
        """
        weight = proj.get('weight')
        delay = proj.get('delay')
        if weight is not None and delay is not None:
            return f"Weight: {weight}, Delay: {delay}"
        elif weight is not None:
            return f"Weight: {weight}"
        elif delay is not None:
            return f"Delay: {delay}"
        return ""

    def _add_input_edge(self, G, input_id, input_info, input_sources):
        """
        Add an input edge to the graph.

        Args:
            G (networkx.DiGraph): The graph to update.
            input_id (str): ID of the input node.
            input_info (dict): Input information.
            input_sources (dict): Dictionary of input sources.
        """
        target_pop = input_info['population']
        #input_params = input_sources[input_info['input_source']]['parameters']
        
        
        G.add_edge(input_id, target_pop, synapse='input', style='solid', arrowstyle='->', color='yellow')

    def _update_node_shapes(self, G, node_synapse_types, node_shapes):
        """
        Update node shapes based on their synapse types.

        Args:
            G (networkx.DiGraph): The graph to update.
            node_synapse_types (dict): Dictionary of node synapse types.
            node_shapes (dict): Dictionary of node shapes.
        """
        # Update node shapes based on their synapse types
        for node, synapse_types in node_synapse_types.items():
            if 'excitatory' in synapse_types and 'inhibitory' in synapse_types:
                G.nodes[node]['shape'] = node_shapes['generic']
            elif 'excitatory' in synapse_types:
                G.nodes[node]['shape'] = node_shapes['excitatory']
                G.nodes[node]['color'] = 'blue'
            elif 'inhibitory' in synapse_types:
                G.nodes[node]['shape'] = node_shapes['inhibitory']
                G.nodes[node]['color'] = 'red'
            elif 'dummy' in synapse_types:
                print(G.nodes[node])
                G.nodes[node]['shape'] = node_shapes['input']
            else:
                G.nodes[node]['shape'] = node_shapes['generic']

    def set_node_positions(self):
        """
        Set the positions of the nodes in a circular layout.

        Returns:
            dict: Node positions.
        """
        pos = {}
        nodes = list(self.G.nodes())
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = math.cos(angle)
            y = math.sin(angle)
            pos[node] = (x, y)
        return pos

    def draw_graph(self):
        """
        Draw the neural network graph.
        """
        pos = self.set_node_positions()
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        max_size = max(data['size'] for _, data in self.G.nodes(data=True))
        scaled_sizes = {}
        
        self._draw_nodes(ax, pos, max_size, scaled_sizes)
        self._draw_edges(ax, pos, scaled_sizes)

        plt.axis('equal')
        plt.axis('off')
        plt.show()

    def _draw_nodes(self, ax, pos, max_size, scaled_sizes):
        """
        Draw nodes on the graph.

        Args:
            ax (matplotlib.axes.Axes): The axes to draw on.
            pos (dict): Node positions.
            max_size (float): Maximum node size.
            scaled_sizes (dict): Dictionary to store scaled node sizes.
        """
        for node, (x, y) in pos.items():
            shape = self.G.nodes[node]['shape']
            color = self.G.nodes[node]['color']
            size = self.G.nodes[node]['size']
            
            scaled_size = self.base_node_size * (size / max_size)
            scaled_sizes[node] = scaled_size
            
            if shape == 's':
                ax.add_patch(plt.Rectangle((x - scaled_size/2, y - scaled_size/2), scaled_size, scaled_size, fill=False, edgecolor=color, linewidth=4))
            elif shape == 'o':
                ax.add_patch(plt.Circle((x, y), scaled_size/2, fill=False, edgecolor=color, linewidth=4))
            elif shape == '^':
                ax.add_patch(plt.Polygon([(x, y + scaled_size/2), (x - scaled_size/2, y - scaled_size/2), (x + scaled_size/2, y - scaled_size/2)], fill=False, edgecolor=color, linewidth=4))
            elif shape == 'h':
                ax.add_patch(RegularPolygon((x, y), numVertices=6, radius=scaled_size/2, fill=False, edgecolor=color, linewidth=4))
            
            ax.text(x, y, node, ha='center', va='center', fontweight='bold')

    def _draw_edges(self, ax, pos, scaled_sizes):
        """
        Draw edges on the graph.

        Args:
            ax (matplotlib.axes.Axes): The axes to draw on.
            pos (dict): Node positions.
            scaled_sizes (dict): Dictionary of scaled node sizes.
        """
        for u, v, d in self.G.edges(data=True):
            start = pos[u]
            end = pos[v]
            color = d['color']
            
            start_x, start_y, end_x, end_y = self._calculate_edge_coordinates(start, end, scaled_sizes[u], scaled_sizes[v])
            
            if d['style'] == 'dashed':
                ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                            arrowprops=dict(arrowstyle="->", color=color, lw=self.edge_width, linestyle="--", mutation_scale=self.mutation_scale))
            else:
                ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                            arrowprops=dict(arrowstyle="->", color=color, lw=self.edge_width, mutation_scale=self.mutation_scale))
            
            if d['synapse'] == 'gabaSyn':
                ax.plot(end_x, end_y, 'o', color=color, markersize=self.edge_width * 10)
            # Check if the edge is not from an input node
            if self.G.nodes[u]['shape'] != 'h' and d['info']:
                try:
                    info = d.get('info', '')
                    if info:
                        mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2

                        ax.text(mid_x, mid_y, info, fontsize=20, ha='center', va='center', backgroundcolor='white')
                except KeyError:
                    # If there's any issue with accessing node or edge properties, we skip adding the text
                    pass
    def _calculate_edge_coordinates(self, start, end, start_size, end_size):
        """
        Calculate the start and end coordinates for an edge.

        Args:
            start (tuple): Start node position.
            end (tuple): End node position.
            start_size (float): Size of the start node.
            end_size (float): Size of the end node.

        Returns:
            tuple: Start and end x and y coordinates for the edge.
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / length, dy / length
        
        start_x = start[0] + dx * start_size / 2
        start_y = start[1] + dy * start_size / 2
        end_x = end[0] - dx * end_size / 2
        end_y = end[1] - dy * end_size / 2
        
        return start_x, start_y, end_x, end_y

