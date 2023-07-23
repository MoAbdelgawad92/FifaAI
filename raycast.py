
import numpy as np

def raycast(targets, current):
    # Extract the x and y coordinates of the specified cell
    x = current.w
    y = current.h
    # get player indices
    x_coords = []
    y_coords = []
    for targ in targets:
        if targ.type == current.type: continue
        x_coords.append(targ.w)
        y_coords.append(targ.h)
    # getting a list of x and a list of y 
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    # Calculate the distances using vectorized operations
    distances = np.sqrt((x_coords - x)**2 + (y_coords - y)**2)
    # Calculate the angles using vectorized operations
    angles = np.arctan2(y_coords - y, x_coords - x) * 180 / np.pi
    # Zip the distances, angles, and values together
    results = np.array([distances,angles]).flatten()

    return results