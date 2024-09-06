# Expose the SimpleNNNetworkGraph class at the package level
from nn_graph.graph import SimpleNNNetworkGraph

# Optionally, include version information
__version__ = "0.1.0"

# If there are other utility functions or constants that need to be exposed,
# they can be imported and exposed here as well, for example:
# from .utils import some_utility_function

# Define the __all__ list to specify what should be imported
# when the user uses `from nn_graph import *`
__all__ = ['SimpleNNNetworkGraph']
