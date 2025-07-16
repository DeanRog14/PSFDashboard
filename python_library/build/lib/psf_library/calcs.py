from datetime import date

'''
Has any sort of math function that we are use relatively often. 
'''

# Creating function so that we calc the cumulative return of the entire df
def compute_df_cumulative(df):
    return (1 + df.drop('date', axis=1)).cumprod() - 1

# Function so that we calculate the cumulative return of a specific column
def compute_col_cumulative(df, col):
    return (1 + df[col]).cumprod() - 1

# Function so that we can calculate the annualied return
def annualized_return(df, col, date1, date2):
    cumulative_return = compute_col_cumulative(df, col)
    # Dates need to be given in this form date(2023, 2, 15)
    difference = date2 - date1
    days = difference.days
    
    return ((1 + cumulative_return) ** (365 / days)) - 1

# Calculates the z-score for a specified column
def z_score(df, col):
    return (df[col].iloc[-1] - df[col].mean()) / df[col].std()

# Adds a percent sign to a value
def to_percent(y, _):
    return f'{y:.0f}%'

# Adds a percent sign to a value
def to_ratio(y, _):
    return f'{y:.0f}x'