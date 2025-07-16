import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd

#### Building subplot pdf ####

# Allows for saving figs off as images to be used later in the building of pdf
def fig_save_load(figures):
    images = []
    
    # Creates the png names and saves them off
    for i, fig in enumerate(figures, start=1):
        file_name = f'fig{i}.png'
        # Saves off at a very low dpi so it loads quicker, this is updated when final pdf or img created
        fig.savefig(file_name, dpi=150,  bbox_inches='tight', pad_inches=0)
        img = mpimg.imread(file_name)
        images.append(img)
        
    # Returns a list of the image names
    return images 

# Adds the image to the subplot
def add_image(ax, img, aspect_auto=True):
    if aspect_auto:
        # The picture will stretch to fill the entire column or space
        ax.imshow(img, aspect='auto')
    else:
        # The picture will take up the space that is specified when loaded
        ax.imshow(img)
    ax.axis('off')

# Plots all the subplots in user specified locations
def plot_images_with_layout(fig, gs, layout, images, add_image_func):
    for location, img in zip(layout, images):
        ax = fig.add_subplot(location)
        add_image_func(ax, img)

    return fig
