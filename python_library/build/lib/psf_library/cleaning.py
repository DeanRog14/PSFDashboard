import pandas as pd
import random
from .calcs import z_score, annualized_return, compute_col_cumulative

'''
Complete data preperation including adding the quarter_year column, creating the z_scores, and selecting only single indexs in their own df's
The z-score allows for adding to the tables, and it's made simpler by placing them into a dictionary for easy use
The prepared df's allow for building graphs with only the specified index in each graph, making for simpler and quicker modeling
The last day of each quarter allows for us to cut the df's based on which quarters we need for analysis, can place prepped df in this function
'''

# Gives information about what kind of data you are dealing with 
def data_info(df):
    print("Shape of the dataset: ")
    print(f"Columns: {df.shape[1]}, Rows: {df.shape[0]}\n")
    print("The total number of N/A values in each column: ")
    print(df.isna().sum(), "\n")
    print("The data types of each column: ")
    print(df.dtypes, "\n")

# Allows you to get a list of unique values for a specific column
def unique_values(df, column, number=None):
    unique_vals = df[column].unique().tolist()
    return unique_vals[:number]

#### PSF COLORS ####
color = ['#DB7628', '#0F3651']

# Allows for getting a random grouping of colors, based on number of colors inputted
def color_selection(number):
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', "#006b2d", "#6b0054", '#bcf60c', 
              "#02ADAD", "#0e0088", '#9a6324', "#A30101", "#42e072", '#808000', "#c56c13", '#000075', '#808080']
    return random.sample(colors, number)

# Adds a column that has the quarter and year combined
def data_prep(df, security, col):
    # Ensures the values are correct and smaller forms for better runtimes
    df['date'] = pd.to_datetime(df['date'])
    df[col] = df[col].astype('float32')

    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter
    
    subset = df[df['security'] == security].copy()
    
    # Concatenates the quarter and year together to create an easy to read notation
    subset['quarter'] = subset['quarter'].astype(str)
    subset['year'] = subset['year'].astype(str)
    subset['quarter_year'] = 'Q' + subset['quarter'] + ' ' + subset['year']    
    
    return subset

# Splits apart the indexes and puts them into a dictionary
def prep_dfs(df, index_list, column_name):
    prepared_dfs = {}

    for index in index_list:
        prepared_dfs[index] = data_prep(df, index, column_name)

    return prepared_dfs

# Creates a z-score, table, and prepared df based on the df, indexs, and column name given
def process_indices(df, index_list, column_name, calc=None, date1=None, date2=None):
    # Creates blank dictionaries to be filled 
    calculation = {}
    tables = {}
    prepared_dfs = {}

    # Iterates over all the values in the index list and creates the specified lists
    for index in index_list:
        # Filter the dataframe based on the index given
        index_df = df[df['security'] == index]

        if (calc == 'z-score'):
            val = z_score(index_df, column_name)
        elif (calc == 'mean'):
            val = index_df[column_name].mean()
        elif (calc == 'annualized return'):
            val = annualized_return(index_df, column_name, date1, date2)
        else:
            val = 0

        calculation[index] = f"{val:.2f}"

        # Store the z-scores in the dataframe for use in tables on graph
        tables[index] = pd.DataFrame({calc: [f"{val:.2f}"]})
        
        # Prepare data with new column and only the specified index
        prepared_dfs[index] = data_prep(df, index, column_name)

    return calculation, tables, prepared_dfs

# Returns only the df with the data at the end of each quarter
def get_last_day_each_quarter(df, start_idx=None, end_idx=None):
    df['date'] = pd.to_datetime(df['date'])
    
    # Selects the year and the quarter based on the given date
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter

    # Finds the maximum date within each quarter and saves them off into a df
    last_dates = df.groupby(['year', 'quarter'])['date'].transform('max')
    # Selects only the last dates from the df which gets us the final df
    filtered_df = df[df['date'] == last_dates]

    # Selects the given range of values based on the inputs to the function
    if start_idx is not None and end_idx is not None:
        return filtered_df.iloc[start_idx:end_idx]
    else:
        return filtered_df