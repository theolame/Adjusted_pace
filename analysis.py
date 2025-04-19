def weighted_average_speed(speeds, distances):
    """
    Calculate the weighted average speed based on distance segments.

    Parameters:
        speeds (list of float): Speed values (in m/s) for each segment.
        distances (list of float): Corresponding distances (in meters) for each segment.

    Returns:
        float: The weighted average speed (in m/s), or 0 if total distance is zero.
    """
    # Ensure both lists have the same length
    if len(speeds) != len(distances):
        raise ValueError("Speed and distance lists must be of equal length.")
    
    # Calculate the total distance covered
    total_distance = sum(distances)
    
    # Compute the weighted average speed: sum of (speed × distance) divided by total distance
    return sum(s * d for s, d in zip(speeds, distances)) / total_distance if total_distance > 0 else 0


def flat_terrain_energy_cost(distances, flat_cost=3.40):
    """
    Estimate energy cost for each segment on flat terrain.

    Parameters:
        distances (list of float): Distances of each segment (in meters).
        flat_cost (float): Constant energy cost per meter on flat terrain (default is 3.40 J/kg/m).

    Returns:
        list of float: Energy cost per segment assuming flat terrain.
    """
    # Compute the energy cost assuming flat terrain, using a constant energy cost value
    return [d * flat_cost for d in distances]


def compute_adjusted_speed(energy_cost, speeds, distances):
    """
    Adjust speed based on energy cost compared to flat terrain.

    Parameters:
        energy_cost (list of float): Actual energy cost for each segment (in J/kg).
        speeds (list of float): Original speeds (in m/s).
        distances (list of float): Distances for each segment (in meters).

    Returns:
        list of float: Adjusted speeds based on energy expenditure.
    """
    # Calculate the flat terrain energy cost for each segment
    flat_energy = flat_terrain_energy_cost(distances)
    
    # Adjust the speed based on the ratio between actual and flat terrain energy cost
    return [s * (ec / fe) for s, ec, fe in zip(speeds, energy_cost, flat_energy)]


def slope_and_speed_by_distance(altitudes, distances, speeds, timestamps, window_distance=50):
    """
    Compute slope and average speed over fixed sliding distance windows.

    Parameters:
        altitudes (list of float): Altitude values (in meters).
        distances (list of float): Cumulative distance values (in meters).
        speeds (list of float): Instantaneous speed values (in m/s).
        timestamps (list of float): Timestamps in minutes from start.
        window_distance (float): Size of each sliding window (in meters).

    Returns:
        list of tuples: Each tuple contains (slope %, avg speed in m/s, distance, timestamp).
    """
    # Compute slope and average speed over moving distance windows (e.g., 50 meters)
    results = []
    i = 0
    n = len(altitudes)

    while i < n:
        j = i + 1
        # Move forward until we reach a window distance or the end of the data
        while j < n and (distances[j] - distances[i] < window_distance):
            j += 1

        if j < n:
            # Compute change in altitude and distance over the window
            delta_alt = altitudes[j] - altitudes[i]
            delta_dist = distances[j] - distances[i]

            # Average speed over the window
            avg_speed = sum(speeds[i:j]) / (j - i)

            # Slope in percent (capped between -40% and +40%)
            slope = max(min((delta_alt / delta_dist) * 100 if delta_dist > 0 else 0, 40), -40)

            # Store slope, average speed, segment distance, and timestamp at window end
            results.append((slope, avg_speed, delta_dist, timestamps[j]))
        else:
            # If we can't compute a window, repeat the last value or default to zero
            results.append(results[-1] if results else (0.0, 0.0, 0.0, timestamps[-1]))

        i += 1

    return results
