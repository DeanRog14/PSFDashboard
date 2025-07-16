import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from datetime import date
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MaxNLocator
from .cleaning import get_last_day_each_quarter
from .calcs import to_percent, to_ratio

'''
All plotting functions are located here including the plotting of the basic subplot, labeling the points, and building the table
The basic subplot is built without any axis information, and the edge of the plot is based on the min and max values
The point labels are added to each point on the line, and can be adjusted with their location/xycords
The table builder adds a table given information from a df and the location can be adjusted based on the needs for the graph
'''

#### Line Graphs ####

# Allows for building simple line graphs on a specified subplot range
def plot_basic_lines(index_list, prepared_dataframes, column, row, subplt_row, subplot_col, figsize, quarterly=None, start_value=None, end_value=None):
    # Sets up the subplot and axes for use
    fig, axes_array = plt.subplots(subplt_row, subplot_col, figsize=figsize, constrained_layout=True)

    # Flattens the axes so we can acess like an array
    if isinstance(axes_array, np.ndarray):
        axes = axes_array.flatten()
    else:
        axes = [axes_array]

    dfs = []

    # Builds each subplot using the prepped dfs
    for i, index in enumerate(index_list):
        ax = axes[i]
        if (quarterly == True):
            df = get_last_day_each_quarter(prepared_dataframes[index], start_value, end_value)
            dfs.append(df)
        else:
            df = prepared_dataframes[index]
            dfs.append(df)

        ax.plot(df[row], df[column])

    # Turn off unused axes
    for i in range(len(index_list), subplt_row * subplot_col):
        axes[i].axis('off')

    return fig, axes, dfs

# Allows for building colored line graphs on a specified subplot range
def plot_colored_lines(index_list, colors, prepared_dataframes, column, row, subplt_row, subplot_col, figsize, quarterly=None, start_value=None, end_value=None):
    fig, axes_array = plt.subplots(subplt_row, subplot_col, figsize=figsize, constrained_layout=True)

    if isinstance(axes_array, np.ndarray):
        axes = axes_array.flatten()
    else:
        axes = [axes_array]

    dfs = []

    # Zips together the index_list and colors so they can be used in tandem when plotting
    for i, (index, color) in enumerate(zip(index_list, colors)):
        ax = axes[i]
        if (quarterly == True):
            df = get_last_day_each_quarter(prepared_dataframes[index], start_value, end_value)
            dfs.append(df)
        else:
            df = prepared_dataframes[index]
            dfs.append(df)

        ax.plot(df[row], df[column], color=color)

    # Turn off unused axes
    for i in range(len(index_list), subplt_row * subplot_col):
        axes[i].axis('off')

    return fig, axes, dfs

# Allows for building line graphs with a colored point on the lines on a specified subplot range
def plot_scatter_lines(index_list, colors, prepared_dataframes, column, row, subplt_row, subplot_col, figsize, mark, quarterly=None, start_value=None, end_value=None):
    fig, axes_array = plt.subplots(subplt_row, subplot_col, figsize=figsize, constrained_layout=True)

    if isinstance(axes_array, np.ndarray):
        axes = axes_array.flatten()
    else:
        axes = [axes_array]

    dfs = []

    for i, (index, color) in enumerate(zip(index_list, colors)):
        ax = axes[i]
        if (quarterly == True):
            df = get_last_day_each_quarter(prepared_dataframes[index], start_value, end_value)
            dfs.append(df)
        else:
            df = prepared_dataframes[index]
            dfs.append(df)

        ax.plot(df[row], df[column], marker=mark, color='black', markerfacecolor=color)

    # Turn off unused axes
    for i in range(len(index_list), subplt_row * subplot_col):
        axes[i].axis('off')

    return fig, axes, dfs

#### Scatterplots ####

# Allows for building simple scatterplot on a specified subplot range
def plot_basic_scatter(index_list, prepared_dataframes, column, row, subplt_row, subplot_col, figsize, quarterly=None, start_value=None, end_value=None):
    # Sets up the subplot and axes for use
    fig, axes_array = plt.subplots(subplt_row, subplot_col, figsize=figsize, constrained_layout=True)

    # Flattens the axes so we can acess like an array
    if isinstance(axes_array, np.ndarray):
        axes = axes_array.flatten()
    else:
        axes = [axes_array]

    dfs = []

    # Builds each subplot using the prepped dfs
    for i, index in enumerate(index_list):
        ax = axes[i]
        # Allows for specification of how many points wanted on subplot
        if (quarterly == True):
            df = get_last_day_each_quarter(prepared_dataframes[index], start_value, end_value)
            dfs.append(df)
        else:
            df = prepared_dataframes[index]
            dfs.append(df)

        ax.scatter(df[row], df[column])

    # Turn off unused axes
    for i in range(len(index_list), subplt_row * subplot_col):
        axes[i].axis('off')

    return fig, axes, dfs

# Allows for building colored scatterplots on a specified subplot range
def plot_colored_scatter(index_list, colors, prepared_dataframes, column, row, subplt_row, subplot_col, figsize, quarterly=None, start_value=None, end_value=None):
    fig, axes_array = plt.subplots(subplt_row, subplot_col, figsize=figsize, constrained_layout=True)

    if isinstance(axes_array, np.ndarray):
        axes = axes_array.flatten()
    else:
        axes = [axes_array]

    dfs = []

    # Zips together the index_list and colors so they can be used in tandem when plotting
    for i, (index, color) in enumerate(zip(index_list, colors)):
        ax = axes[i]
        if (quarterly == True):
            df = get_last_day_each_quarter(prepared_dataframes[index], start_value, end_value)
            dfs.append(df)
        else:
            df = prepared_dataframes[index]
            dfs.append(df)
        
        ax.scatter(df[row], df[column], color=color)


    # Turn off unused axes
    for i in range(len(index_list), subplt_row * subplot_col):
        axes[i].axis('off')

    return fig, axes, dfs

#### Tables ####

# Builds a table on a specified ax
def table_builder(df_table, ax, location):
    table = ax.table(cellText=df_table.values, 
                             colLabels=df_table.columns, 
                             loc=location, cellLoc='center')
    # Specific font selections so all the tables are identical in looks
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(.12, 1.2)


#### Styling axes ####

# Works for building a plot with just the basic x and y axis from the plotting
def simple_axes(ax, title):
    ax.set_title(title, fontweight='bold')


# Works for building a plot with just a title and nothing else
def style_axes_blank(ax, title):
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel(' ')
    ax.set_xlabel(' ')
    ax.set_xticks([])
    ax.set_yticks([])

# Works for styling with a date on x-axis and allows either (% or x) formatting on y-axis
def style_axes_date(ax, df, title, ending, dateperiods, format):
    ax.set_title(title, fontweight='heavy', style='italic')

    ax.tick_params(labelsize=12)
    ax.set_ylabel('')

    # Allows for easy formatting of percent or ratio on y-axis
    if ending == 'percent':
        ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    elif ending == 'ratio':
        ax.yaxis.set_major_formatter(FuncFormatter(to_ratio))

    ax.yaxis.set_major_locator(MaxNLocator(nbins=4, prune=None))

    start_date = df['date'].iloc[0]
    end_date = df['date'].iloc[-1]

    # Allows for selection of the time period shown on x-axis, along with formatting
    tick_dates = pd.date_range(start=start_date, end=end_date, periods=dateperiods)
    ax.set_xticks(tick_dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(format))

#### Annotating Values ####

# Works for labeling a single or many points on a specified subplot
def point_label(indices, df, ax, location, xcord, ycord, value1=None, row=None, value2=None):
    # Looks to see if the indices given are an int
    if isinstance(indices, int):
        # If True, then it creates a range from zero to the int
        indices = [indices]
    # If False, then it goes straight to this for loop
    for i in indices:
        # If no values are given nothing happens
        if value1 is None and value2 is None:
            break

        # If one value is given to annotate then also need to specify row value, so annotation can be placed correctly
        elif value1 is not None and value2 is None:
            y = df[value1].iloc[i]
            x = df[row].iloc[i]

            label = f'{y:.2f}'
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(xcord, ycord),
                    ha=location, fontsize=7)

        # If both values are given then annotation is shown    
        else:
            y = df[value1].iloc[i]
            x = df[value2].iloc[i]

            label = f"   {y:.2f} \n {x}"
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(xcord, ycord),
                        ha=location, fontsize=7)


#################################

# Calls all of the other building functions so that we can piece together the graphs, and the tables
def annotate_on_lines(index_list, colors, prepared_dataframes, tables, column, row, subplt_row, subplot_col, figsize, putTables):
    # fig, axes = create_subplots(subplt_row, subplot_col, figsize)
    fig, axes_array = plt.subplots(subplt_row, subplot_col, figsize=figsize, constrained_layout=True)
    
    if isinstance(axes_array, np.ndarray):
        axes = axes_array.flatten()
    else:
        axes = [axes_array]
    
    # Iterates through the indexes and colors to build each plot
    for i, (index, color) in enumerate(zip(index_list, colors)):
        # Gives us easy access to the values we will be using a lot
        ax = axes[i]

        # Creates the cleaned and shortened dataframe based on the specific index
        df = get_last_day_each_quarter(prepared_dataframes[index])

        # Plots the line graph with the points
        plot_ratio(ax, df, index, color, column, row)

        # Creates the table in the bottom corner 
        if (putTables == True):
            table_builder(tables[index], ax, 'lower right')
        elif (putTables == False):
            continue

        # Iterates over each value in the df and annotates it based on a certain structure
        for i in range(0, len(df)):
            # Sets up the values we will be working with
            curr_val = df[column].iloc[i]
            
            if (i > 0) :
                prev_val = df[column].iloc[i - 1]

            if (i + 1) < len(df):
                next_val = df[column].iloc[i + 1]

            # Goes through each value and decides where the annotation should go
            if i == 0:
                if curr_val < next_val:
                    point_label(i, df, ax, 'left', 2, -12, row, column)
                else:
                    point_label(i, df, ax, 'left', 0, 4, row, column)
        
            elif i == 1:
                if (curr_val > prev_val) and (curr_val < next_val) and (next_val - curr_val) > 0.05:
                    point_label(i, df, ax, 'left', 2, -15, row, column)
                elif (curr_val < prev_val) and (curr_val < next_val):
                    point_label(i, df, ax, 'left', 2, -15, row, column)
                elif (curr_val - prev_val) > 0.5:
                    point_label(i, df, ax, 'left', 0, 4,row,  column)
                elif (curr_val - prev_val) == 0:
                    point_label(i, df, ax, 'left', 2, -12,row,  column)
                else:
                    point_label(i, df, ax, 'right', 0, 4,row,  column)
        
            elif i == 2:
                if (prev_val - curr_val) < 0.35 and (next_val < curr_val):
                    point_label(i, df, ax, 'left', 0, 4, row, column)
                elif (prev_val - curr_val) < 0.5 or (next_val - curr_val) >= 1 or (curr_val < prev_val and curr_val < next_val):
                    point_label(i, df, ax, 'left', 2, -15,row,  column)
        
            elif i == 3:
                if (prev_val - curr_val) < 0.35 and (next_val < curr_val):
                    point_label(i, df, ax, 'left', 0, 4,row,  column)
                else:
                    point_label(i, df, ax, 'left', 2, -15, row, column)
        
            elif i == 4:
                point_label(i, df, ax, 'left', 0, 4,row,  column)

    # Removes the additional axes that are not being used
    for i in range(len(index_list), subplt_row * subplot_col):
        axes[i].axis('off')
    plt.show()



def annotate_on_scatter(ax, points, labels, ydist, xdist, offset=0.25, fontsize=8):
    min_x = min(px for px, py in points)
    max_x = max(px for px, py in points)
    min_y = min(py for px, py in points)
    max_y = max(py for px, py in points)
    
    for (x, y), label in zip(points, labels):
        has_point_right = any((px > x and abs(px - x) < xdist and abs(py - y) < ydist) 
                              for px, py in points 
                              if (px, py) != (x, y))
        has_point_left  = any((px < x and abs(px - x) <= xdist and abs(py - y) < ydist) 
                              for px, py in points 
                              if (px, py) != (x, y))
        has_point_above = any((py > y and abs(py - y) < ydist and abs(px - x) < xdist) 
                              for px, py in points 
                              if (px, py) != (x, y))
        has_point_below = any((py < y and abs(py - y) < ydist and abs(px - x) < xdist) 
                              for px, py in points 
                              if (px, py) != (x, y))
    
        dx = -offset if has_point_right and not has_point_left else offset
        dy = -offset if has_point_above and not has_point_below else offset
    
        if has_point_right and has_point_left:
            dx = offset
        if has_point_above and has_point_below:
            dy = offset
    
        if len(label) > 17:
            dx = -offset
            
        if x == min_x:
            dy = -offset
            va = 'top'
        elif x == max_x:
            dx = -offset
            ha = 'right'
        else:
            ha = 'left' if dx > 0 else 'right'
    
        if y == max_y:
            dy = -offset 
            va = 'top'
        elif y == min_y:
            dy = offset
            va = 'bottom'
        else:
            if x != min_x:
                va = 'bottom' if dy > 0 else 'top'
    
        tx, ty = x + dx, y + dy
    
        plt.annotate(label,
                     xy=(x, y), xytext=(tx, ty),
                     fontsize=fontsize, ha=ha, va=va)
    plt.show()