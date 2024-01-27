=# Quantitative Trading Algorithm Project

## Overview
This project focuses on statistical arbitrage and pairs trading. It involves selecting stock pairs, performing preliminary analysis to identify valid pairs, and conducting various financial analyses.

## Setup and Installation
- Ensure Python 3.x is installed.
- Clone the repository: `git clone [repository-url]`
- Navigate to the project directory and set up the virtual environment:
  - `python -m venv venv`
  - Activate the environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`
- Set up a PostgreSQL database (instructions).

## Usage
- Run the data collection script: `python src/data_collection.py`
- Execute analysis scripts to generate financial metrics.

## Features
- Data Collection from Yahoo Finance
- Pearson Coefficient Calculation
- Augmented Dickey-Fuller Test
- Beta Coefficient Calculation
- Sharpe Ratio Calculation
- Hurst Exponent Calculation
- (Optional) Monte Carlo Simulation

## Contributing
Feel free to fork the project and submit pull requests.

## License
