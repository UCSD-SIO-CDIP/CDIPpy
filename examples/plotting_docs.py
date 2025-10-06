"""
CDPpy: Plotting and Data Visualization Documentation
-----------------------------------------------------

This script demonstrates how to use CDPpy's built-in plotting and
data visualization methods to explore and analyze cell culture data.
"""

from cdippy import CDPpy

# Initialize CDPpy object
cdp = CDPpy()

# Sample cell culture data
data = {
    'time': [0, 1, 2, 3, 4, 5],
    'cell_density': [1.0, 1.2, 1.5, 1.9, 2.2, 2.5],
    'glucose_concentration': [5.0, 4.8, 4.5, 4.2, 4.0, 3.8]
}

# -----------------------------
# Basic Analysis
# -----------------------------
results = cdp.analyze(data)
print("Analysis Results:")
print(results)

# -----------------------------
# Plotting Methods
# -----------------------------

# 1. Plot a single variable against time
cdp.plot(
    data, 
    x='time', 
    y='cell_density', 
    title='Cell Density Over Time',
    xlabel='Time (hours)',
    ylabel='Cell Density (cells/mL)'
)

# 2. Plot another variable
cdp.plot(
    data,
    x='time',
    y='glucose_concentration',
    title='Glucose Concentration Over Time',
    xlabel='Time (hours)',
    ylabel='Glucose Concentration (mM)'
)

# 3. Plot multiple variables together (if supported)
cdp.plot_multiple(
    data,
    y=['cell_density', 'glucose_concentration'],
    title='Cell & Glucose Dynamics Over Time',
    xlabel='Time (hours)'
)

# -----------------------------
# Notes:
# -----------------------------
# - `plot()` is used for a single variable.
# - `plot_multiple()` is used to compare multiple variables in one figure.
# - Always include descriptive titles and axis labels for clarity.
