# example_script.py
# Demonstrating basic usage of CDPpy for analyzing cell culture data

from cdippy import CDPpy  # Import the CDPpy library

# Initialize the CDPpy object
cdp = CDPpy()

# Sample data representing cell culture measurements
data = {
    'time': [0, 1, 2, 3, 4],
    'cell_density': [1.0, 1.2, 1.5, 1.8, 2.0],
    'glucose_concentration': [5.0, 4.8, 4.5, 4.2, 4.0]
}

# Analyze the data using CDPpy's built-in methods
analysis_results = cdp.analyze(data)

# Print the analysis results
print("Analysis Results:")
print(analysis_results)
