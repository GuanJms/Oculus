"""
This scrip is used to read, sort and store the csv file.
"""
import glob
import pandas as pd
import os
from configuration_module.configuration_manager import ConfigurationManager


# Root path to the project data
root_path = ConfigurationManager.get_root_system()

# Pattern to match all 'raw_traded_quote' directories for each ticker
pattern = os.path.join(root_path, 'USO_sorted_test', 'raw_traded_quote', '*','*','*.csv')

# Find all CSV files in 'raw_traded_quote' directories
csv_files = glob.glob(pattern, recursive=True)

# Process each CSV file
for file_path in csv_files:
    # Read the CSV file
    df = pd.read_csv(file_path)
    # print(file_path)

    # Sort the DataFrame by 'ms_of_day'
    df_sorted = df.sort_values(by='ms_of_day')

    # Save the sorted DataFrame back to the same file
    df_sorted.to_csv(file_path, index=False)
