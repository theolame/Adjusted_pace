import math
import matplotlib.pyplot as plt

def speed_to_pace_min_per_km(speed):
    """
    Convert speed (in m/s) to pace (in min/km).

    Parameters:
        speed (float): Speed in meters per second.

    Returns:
        float or None: Pace in minutes per kilometer, or None if speed is zero or negative.
    """
    # Convert speed in m/s to pace in min/km, handling invalid or zero speed
    return (1000 / speed) / 60 if speed and speed > 0 else None


def haversine(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance between two points using the Haversine formula.

    Parameters:
        lat1 (float): Latitude of point 1 in degrees.
        lon1 (float): Longitude of point 1 in degrees.
        lat2 (float): Latitude of point 2 in degrees.
        lon2 (float): Longitude of point 2 in degrees.

    Returns:
        float: Distance between the two points in meters.
    """
    # Earth's radius in meters
    R = 6371000

    # Convert latitude and longitude from degrees to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)

    # Apply Haversine formula
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Return the distance in meters
    return R * c


def plot(x, y, title, xlabel, ylabel):
    """
    Plot a simple 2D line graph using matplotlib.

    Parameters:
        x (list): Values for the x-axis.
        y (list): Values for the y-axis.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.

    Returns:
        None: Displays the plot.
    """
    # Create a new figure with fixed size
    plt.figure(figsize=(10, 5))

    # Plot x vs y
    plt.plot(x, y)

    # Set plot title and axis labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Add grid and adjust layout
    plt.grid()
    plt.tight_layout()

    # Display the plot
    plt.show()
