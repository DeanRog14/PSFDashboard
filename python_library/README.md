# Texas PSF Library

The goal behind this library is to have  shortcuts for commonly used functions or actions

Different Packages:
1. Cleaning - getting basic info about data and cleaning any data
2. Calculations - simple finance calculations
3. Plotting - different plotting types and making look pretty 

## Installation

To install: 

`pip install python-libary`

path should be the location of where you have the library located in your computer

## How to import different packages

```python
import psf_library as psf
import psf_library.cleaning as psf_clean
import psf_library.calcs as psf_calc
import psf_library.plotting as psf_plot
```

## Getting started

Start with uploading a csv:

` cpi_df = pd.read_csv("CPI.csv") `

We can then view relevant info within the dataset:
``` python
psf_clean.data_info(cpi_df) 

# Shape of the dataset: 
# Columns: 5, Rows: 404

# The total number of N/A values in each column: 
# date        0
# security    0
# PX_LAST     0
# year        0
# quarter     0
# dtype: int64 

# The data types of each column: 
# date        datetime64[ns]
# security            object
# PX_LAST            float32
# year                 int32
# quarter              int32
# dtype: object 
```

## Cleaning and viewing

Simple way to get started with splitting our indexes into their own df, inclosed within a dictionary:
``` python 
prepared_dataframes = psf_clean.prep_dfs(cpi_df, index_list, 'PX_LAST')

# {'EHPIEU Index':           date      security  PX_LAST  year  quarter quarter_year
#  0   2015-03-31  EHPIEU Index    -0.33  2015        1      Q1 2015
#  11  2015-06-30  EHPIEU Index     0.43  2015        2      Q2 2015
#  20  2015-09-30  EHPIEU Index     0.37  2015        3      Q3 2015
#  33  2015-12-31  EHPIEU Index     0.27  2015        4      Q4 2015 }
```

Can view each individual index df outside the dictionary like this:
``` python 
prepared_dataframes['EHPIEU Index']

#       date	    security	    PX_LAST	year quarter quarter_year
# 0     2015-03-31	EHPIEU Index	-0.33	2015	1	Q1 2015
# 11	2015-06-30	EHPIEU Index	0.43	2015	2	Q2 2015
# 20	2015-09-30	EHPIEU Index	0.37	2015	3	Q3 2015
# 33	2015-12-31	EHPIEU Index	0.27	2015	4	Q4 2015
```

Get unique values of a certain column as a list:
``` python 
index_list = psf.unique_values(cpi_df, 'security')
# ['EHPIEU Index', 'CNCPIYOY Index', 'JNCPIYOY Index', 'CPI YOY Index']
```

Splits dfs and creates a table along with a calculation:

``` python 
mean, tables, prepared_dataframes = psf_clean.process_indices(cpi_df, index_list,'PX_LAST', 'mean')

mean
# {'EHPIEU Index': '2.39',
#  'CNCPIYOY Index': '1.56',
#  'JNCPIYOY Index': '1.13',
#  'CPI YOY Index': '2.93'}

tables 
# {'EHPIEU Index':    mean
#  0  2.39,
#  'CNCPIYOY Index':    mean
#  0  1.56,
#  'JNCPIYOY Index':    mean
#  0  1.13,
#  'CPI YOY Index':    mean
#  0  2.93}
```

## Plotting

### Types of plots
Plots a simple 2x2 subplot, with PX_LAST on y-axis, and date on x-axis:
``` python
# Builds the basic line plot with the indexes, dfs, column, row, subplot rows/columns, and figure size
fig, axes, dfs = psf_plot.plot_basic_lines(index_list, prepared_dataframes, 'PX_LAST', 'date', 2, 2, (12,8))

# Plots the graphs and labels them, using the index as the title, and the column/row for x/y axis
for ax, df, index in zip(axes, dfs, index_list):
    psf_plot.simple_axes(ax, index)
```

All line plots can have data sliced if needed:
``` python 
# Can set if you want the data to be quarterly if possible, then set a range for the values
quarterly=None, start_value=None, end_value=None

# Sets to quarterly and plots the first 5 data points
plot_basic_lines(index_list, prepared_dataframes, 'PX_LAST', 'date', 2, 2, (12,8), True, 0, 5)
```

Can plot different types, depending on usecase: 
``` python
# Use this to easily get a colors for a colored plot
colors = psf.color_selection(4)

plot_colored_lines(index_list, colors, prepared_dataframes, column, row, subplt_row, subplot_col, figsize)

# Select mark="o" and you will get a dot on the line at each value
plot_scatter_lines(index_list, colors, prepared_dataframes, column, row, subplt_row, subplot_col, figsize, mark)

plot_basic_scatter(index_list, prepared_dataframes, column, row, subplt_row, subplot_col, figsize)

plot_colored_scatter(index_list, colors, prepared_dataframes, column, row, subplt_row, subplot_col, figsize)
```

### Axis styling
Allows for styling of the axes based on what the plot needs:
``` python 
# Uses the row and column from the plotting on the x-axis and y-axis labels, uses index for title
psf_plot.simple_axes(ax, index)

# Removes all axis labels and ticks leaving them blank, only a title and the subplot box 
psf_plot.style_axes_blank(ax, index)

# Sets the y-axis to be a ratio ex. "10x", has 5 time periods on x-axis, and sets date to be in year format
psf_plot.style_axes_date(ax, df, title, 'ratio', 5, '%Y')
```
### Annotations
Allows for labeling one or many points along a line or on a scatterplot:
``` python 
# Set the amount of points to label, the location, and the value for the label
psf_plot.point_label(range(10), df, ax, 'right', 0, 0, value1='PX_LAST', row='date')
```

### Table builder
Adding a table to the graph based on given calculation from cleaning:
``` python 
# Uses the tables value for the index, and places in a location specified by the function
psfplot.table_builder(tables[index], ax, 'lower right')
```

### Recommended use case
Build the plots first, then loop over and label the axes/points/tables:
``` python
fig, axes, dfs = psf_plot.plot_scatter_lines()

for ax, df, title in zip(axes, dfs, index_list):
    psf_plot.simple_axes()
    psf_plot.point_label()
    psf_plot.table_builder()
```

## Putting it all together

1. Start with loading and viewing the csv
2. Make any data type, variable changes, or dealing with missing values
3. Prep the dfs so that they are ready to be plotted
4. Get uniques and/or colors based on the type of graph you want to build
5. Use plotting function to graph ensuring any necessary variables are added
6. Add the axes and point labels/tables