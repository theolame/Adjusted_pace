from data_extraction import DataExtractor
from analysis import slope_and_speed_by_distance, compute_adjusted_speed, weighted_average_speed
from minetti_model import MinettiModel
from utils import speed_to_pace_min_per_km, plot

# This function loads the data from the input file and returns the extracted data
def load_data(filepath):
    """
    Extract data (timestamps, altitudes, speeds, and distances) from a given file.
    
    Parameters:
    - filepath (str): Path to the input file (either .fit or .gpx)
    
    Returns:
    - tuple: (timestamps, altitudes, speeds, distances)
    """
    extractor = DataExtractor(filepath)
    return extractor.extract()

# This function computes the energy costs and adjusted speeds based on the extracted data
def compute_energy_and_adjusted_speed(timestamps, altitudes, speeds, distances):
    """
    Compute energy costs, adjusted speeds, and paces based on the data.
    
    Parameters:
    - timestamps (list): List of timestamps corresponding to each data point
    - altitudes (list): List of altitude values
    - speeds (list): List of speed values
    - distances (list): List of distance values
    
    Returns:
    - tuple: (adjusted_timestamps, slopes, cr_values, adjusted_speeds, adjusted_paces, avg_speeds, adjusted_distances)
    """
    # Initialize the Minetti model to compute energy costs
    model = MinettiModel()
    
    # Calculate slopes and average speeds for each window of data
    slope_speed = slope_and_speed_by_distance(altitudes, distances, speeds, timestamps, window_distance=10)
    slopes, avg_speeds, adjusted_distances, adjusted_timestamps = zip(*slope_speed)

    # Calculate energy cost (cr) for each slope
    cr_values = [model.get_energy_cost(s) for s in slopes]
    
    # Calculate energy cost per distance (J/kg/m)
    energy_costs = [cr * d for cr, d in zip(cr_values, adjusted_distances)]
    
    # Compute the adjusted speed based on energy costs
    adjusted_speeds = compute_adjusted_speed(energy_costs, avg_speeds, adjusted_distances)
    
    # Convert adjusted speed to adjusted pace (min/km)
    adjusted_paces = [speed_to_pace_min_per_km(s) for s in adjusted_speeds]

    return adjusted_timestamps, slopes, cr_values, adjusted_speeds, adjusted_paces, avg_speeds, adjusted_distances

# This function plots the results
def plot_results(timestamps, slopes, cr_values, adjusted_speeds, adjusted_paces):
    """
    Plot the results of the analysis: energy cost vs. slope, adjusted speed, and adjusted pace.
    
    Parameters:
    - timestamps (list): List of adjusted timestamps
    - slopes (list): List of slopes for each data window
    - cr_values (list): List of energy costs (J/kg/m)
    - adjusted_speeds (list): List of adjusted speeds
    - adjusted_paces (list): List of adjusted paces (min/km)
    """
    # Plot energy cost vs slope
    plot(timestamps, cr_values, "Energy Cost vs Slope", "Time (min)", "Cost (J/kg/m)")
    
    # Plot adjusted speed over time
    plot(timestamps, adjusted_speeds, "Adjusted Speed", "Time (min)", "Speed (m/s)")
    
    # Plot adjusted pace over time
    plot(timestamps[:-60], adjusted_paces[:-60], "Adjusted Pace", "Time (min)", "Pace (min/km)")

# This function prints the summary of average pace calculations
def print_summary(adjusted_speeds, avg_speeds, speeds, adjusted_distances, distances):
    """
    Print the summary of average pace calculations.
    
    Parameters:
    - adjusted_speeds (list): List of adjusted speeds
    - avg_speeds (list): List of average speeds per segment
    - speeds (list): List of raw speeds
    - adjusted_distances (list): List of adjusted distances
    - distances (list): List of raw distances
    """
    print("Adjusted Avg Pace:", speed_to_pace_min_per_km(weighted_average_speed(adjusted_speeds, adjusted_distances)))
    print("Raw Avg Pace (Segments):", speed_to_pace_min_per_km(weighted_average_speed(avg_speeds, adjusted_distances)))
    print("Raw Avg Pace (Overall):", speed_to_pace_min_per_km(weighted_average_speed(speeds, distances[:len(speeds)])))

# This is the main function that ties everything together
def run_minetti_analysis(input_file):
    """
    Run the Minetti model analysis pipeline on the given input file.
    
    Parameters:
    - input_file (str): Path to the input file (either .fit or .gpx)
    """
    # Load the data from the input file
    timestamps, altitudes, speeds, distances = load_data(input_file)
    
    # Compute energy costs, adjusted speeds, and paces
    results = compute_energy_and_adjusted_speed(timestamps, altitudes, speeds, distances)
    adjusted_timestamps, slopes, cr_values, adjusted_speeds, adjusted_paces, avg_speeds, adjusted_distances = results
    
    # Plot the results
    plot_results(adjusted_timestamps, slopes, cr_values, adjusted_speeds, adjusted_paces)
    
    # Print the summary of average pace calculations
    print_summary(adjusted_speeds, avg_speeds, speeds, adjusted_distances, distances)

# Example usage
if __name__ == "__main__":
    print("Running analysis on 10k.gpx")
    run_minetti_analysis("data/10k.gpx")
    print("\nRunning analysis on Trail_7lo.fit")
    run_minetti_analysis("data/Trail_7lo.fit")
    print("\nRunning analysis on training.fit")
    run_minetti_analysis("data/training.fit")
