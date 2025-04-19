# Minetti Slope-Adjusted Speed Analysis

This Python project analyzes running activities recorded in `.gpx` or `.fit` format and adjusts the athlete's speed and pace based on terrain slope, using the **Minetti energy cost model**. It provides visualizations of energy cost, adjusted speed, and adjusted pace throughout the activity.

---

## Features

- Parses GPS data from `.gpx` and `.fit` files  
- Computes slope from altitude and distance data  
- Estimates energy cost per meter using the **Minetti CR model**  
- Adjusts speed based on slope-related energy demands  
- Calculates and compares:
  - Raw average pace  
  - Adjusted average pace (Minetti-corrected)  
- Generates plots for:
  - Energy cost vs. slope over time  
  - Adjusted speed over time  
  - Adjusted pace over time  

---

## Project Structure

```
├── main.py                 # Entry point of the program
├── data_extraction.py      # Handles parsing of .fit and .gpx files
├── analysis.py             # Core analysis logic (slope, energy cost, adjusted speed)
├── minetti_model.py        # Encapsulates Minetti's CR model
├── utils.py                # Utility functions (e.g. haversine, plotting)
├── README.md               # This file
```

---

## Requirements

- Python ≥ 3.7  
- Libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `fitparse`
  - `gpxpy`

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

---

## How to Run

Place your .gpx or .fit activity file in the project directory.

Run the analysis script:

python main.py

The script will:

  - Print raw and adjusted average pace

  - Show plots of energy cost, adjusted speed, and adjusted pace
  
---

## Minetti Model

The Minetti model relates slope to the cost of transport (CR) in J/kg/m:

  Downhill is less costly up to a point, then becomes inefficient

  Uphill running costs increase with slope

  The model is interpolated using a cubic spline between known CR values

---

## Sample Data

This project was tested using real running activities from my own Strava profile:
[My Strava Profile](https://www.strava.com/athletes/41811421)

---

## Acknowledgments

  Developed as part of a research project on performance correction based on terrain

  Energy cost model based on research by Minetti et al. (1995)


