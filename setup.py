from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nn_graph",
    version="0.1",
    description="A library for creating and visualizing neural network graphs based on JSON model descriptions.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/nn_graph",  # Replace with your repository URL
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "matplotlib>=3.0",
        "networkx>=2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)