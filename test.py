import matplotlib.pyplot as plt
import numpy as np


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))


import matplotlib.pyplot as plt
import numpy as np

def generate_green_gradient(values):
    for value in values:
        color = (1-value, 1, 1-value)  # Generate a tuple in the format (R, G, B) for green
        plt.plot([0, 1], [value, value], color=color, linewidth=10)

    plt.gca().axis('off')  # Turn off axis
    plt.show()

# Example usage
values = np.linspace(0, 1, 10)  # Generates 10 values between 0 and 1
generate_green_gradient(values)

