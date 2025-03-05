# Gold Price Analysis Project

## Overview

This project is designed to analyze and visualize gold price gaps between different markets, specifically focusing on the Shanghai Gold Exchange (AU) and COMEX Gold Futures (GC). It calculates price differentials, analyzes historical trends, and provides visualization tools for analyzing the gold market.

## Features

- Calculate price gaps between spot gold prices and futures contracts
- Convert between USD and RMB prices using exchange rate data
- Calculate time-to-expiry metrics for futures contracts
- Visualize price gaps with detailed charts
- Real-time market data display using WindPy API (in demo.py)

## Project Structure

```
├── cal_gap.py              # Main calculation script for price gaps
├── plot.py                 # Plotting functionality for visualization
├── demo.py                 # Real-time market data display using WindPy
├── transform_time_format.py # Date format standardization utility
├── requirements.txt        # Project dependencies
├── data/                   # Input data directory
│   ├── AU*.csv             # Shanghai Gold Exchange futures data
│   ├── GC*.csv             # COMEX Gold futures data
│   ├── SPTAUUSDOZ.IDC.csv  # Spot gold prices in USD
│   ├── USDCHY.EX.csv       # USD/CNY exchange rate data
│   └── OpeningPrice.csv    # Opening price data
├── results/                # Output results directory
│   └── price_gaps_*.csv    # Calculated price gap data
└── figs/                   # Generated figures
    └── price_gaps_plot_*.png # Price gap visualization charts
```

## Dependencies

The project requires the following Python packages:

```
numpy
pandas
matplotlib
PyQt5 (for demo.py)
WindPy (for demo.py)
```

## Installation

1. Clone this repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. For the demo, you'll need to install WindPy separately and have a valid Wind Financial Terminal subscription

## Usage

### Calculating Price Gaps

To calculate the price gap for a specific AU contract:

```python
from cal_gap import calculate_gap

# Calculate for AU2412 contract
calculate_gap("AU2412")
```

For COMEX Gold contracts:

```python
from cal_gap import calculate_gc_gap

# Calculate for GCM24E.CMX contract
calculate_gc_gap("GCM24E.CMX")
```

### Generating Visualizations

To plot the calculated price gaps:

```python
from plot import plot_gaps

# Plot the gaps for a specific contract
plot_gaps("results/price_gaps_AU2412.csv")
```

### Running the Demo Application

The demo provides a real-time display of market data:

```bash
python demo.py
```

This launches a GUI application that shows:

- Current bids and asks for selected products
- Price differences between products
- Automated data collection during trading hours

## Data Format

The project expects CSV files with specific formats:

- Gold futures data with columns: DateTime, open, high, low, close, volume
- Exchange rate data with similar structure
- All DateTime fields should be in 'YYYY-MM-DD HH:MM:SS' format

If you have data in a different format, use the transform_time_format.py utility:

```bash
python transform_time_format.py
```

## Contract Naming Convention

- AU contracts: AU + YY + MM (e.g., AU2412 for December 2024)
- GC contracts: GC + M + YY + E.CMX (e.g., GCM24E.CMX for June 2024)
  - Where M is the month code (M=June, Z=December, etc.)

## License

[To be updated]

## Contact

[To be updated]
