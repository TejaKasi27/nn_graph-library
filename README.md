# nn_graph-library

`nn_graph` is a Python library designed for automating the generation of network graph visualizations for simple neuronal models encoded in JSON format. This library is particularly valuable for researchers in computational neuroscience, enabling them to visualize neuronal networks clearly and efficiently.

## Features
- **Automated Graph Generation**: Easily generate network diagrams from JSON-based models.
- **Graph Customization**: Flexible options to customize node sizes, edge styles, colors, and more.
- **NeuroMLlite Compatible**: Built to work seamlessly with models described in JSON format, including those in NeuroMLlite.
- **NEST Support**: Complements NEST (NEural Simulation Tool) by adding enhanced visual representations of network structures.

## Directory Structure
The structure of the nn_graph repository is as follows:

```bash
nn_graph/
│
├── nn_graph/                  # Core library directory
│   ├── __init__.py            # Initialization file for the package
│   └── graph.py               # Main logic for creating and visualizing graphs
│
├── tests/                     # Test files for the package
│   └── test_graph.py          # Unit tests for graph creation
│
├── venv/                      # Virtual environment (not to be included in production)
│
├── LICENSE.txt                # License file for the project
├── README.md                  # Readme file (this file)
├── setup.py                   # Setup file for packaging and installation
└── test.py                    # Script for testing functionality

## Installation
To install the nn_graph library locally, follow the steps below:

Step 1: Clone the Repository
bash
git clone https://github.com/TejaKasi27/nn_graph.git
cd nn_graph

### Step 2: Create a Virtual Environment

It is recommended to use a virtual environment to avoid dependency conflicts:

```bash
python -m venv venv


Step 3: Activate the Virtual Environment
On Windows:

bash
.\venv\Scripts\activate
On macOS/Linux:

bash
source venv/bin/activate

Step 4: Install Dependencies
Install the required dependencies using pip. These are listed in the setup.py and can be installed via:

bash
pip install -r requirements.txt
Alternatively, you can install dependencies through the setup.py script:

bash
pip install -e .

Usage
Once installed, you can use the nn_graph library to create and visualize network graphs. Here's a basic usage example:

python
from nn_graph import SimpleNNNetworkGraph

# Path to your JSON model file
file_path = "Example4_PyNN.json"

# Initialize the graph with options
graph = SimpleNNNetworkGraph(file_path, show_info=True)

# Draw and display the graph
graph.draw_graph()
In this example:

The SimpleNNNetworkGraph class is used to load the network description from a JSON file.
You can customize the graph appearance by passing parameters like show_info for showing additional edge information.
Running Tests
Tests for nn_graph are located in the tests/ directory. You can run the tests with the following command:

bash
python -m unittest discover tests
This command will execute all the unit tests in the tests/ directory.

License
This project is licensed under the MIT License - see the LICENSE.txt file for details.

Contributing
Contributions are welcome! If you'd like to contribute, feel free to fork the repository, make improvements, and submit a pull request.

Acknowledgments
This project was developed as part of an initiative to provide automated tools for visualizing neuronal networks. Special thanks to the computational neuroscience community for providing the foundation for this work.
