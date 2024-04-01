# Quantitative Trading Algorithm Project

## Overview
This project implements a pairs trading strategy designed to identify and exploit temporary price divergences between correlated stocks.  Key concepts include:
- Statistical Arbitrage: A trading strategy that attempts to profit from statistically significant price discrepancies between related assets.
- Pairs Trading: A type of statistical arbitrage that focuses on trading pairs of highly correlated stocks.
- Mean Reversion: The assumption that stock prices tend to revert to their historical mean over time.

## Setup and Installation
- Ensure Python 3.x is installed.
- Clone the repository: `git clone [repository-url]`
- Navigate to the project directory and set up the virtual environment:
  - `python -m venv venv`
  - Activate the environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`

## Usage
- Run the analysis script: `python main.py`
- This script will guide you through data collection, analysis, and potential trade identification.

## Features
- Data Collection from Yahoo Finance: Fetches historical stock price data using the yfinance API.
- Pearson Coefficient Calculation: Measures the linear correlation between two stocks. A high correlation suggests a potential pairs trading opportunity.
- Augmented Dickey-Fuller (ADF) Test: Tests for stationarity in time series data.  Stationarity is often a sign of mean-reversion tendencies.
- Beta Coefficient Calculation: Measures the volatility of a stock relative to the overall market.  Used to understand the risk profile of the trading pair.
- Sharpe Ratio Calculation: Evaluates the risk-adjusted return of a potential trade.
- Half-Life:  Indicates the expected time it takes for a temporary price divergence to correct itself.
- Hurst Exponent Calculation: Analyzes the long-term memory of a stock's price movements.
  - A Hurst exponent of 0.5 indicates a random walk (no persistent trend).
  - A value greater than 0.5 suggests a positive trend (prices tend to move in the same direction).
  - A value less than 0.5 implies a mean-reverting tendency (prices tend to revert back to their historical mean).

## Optional PostegreSQL Integration

For users who wish to store and manage the collected data within a PostgreSQL database, the project provides the necessary setup instructions and schema definitions.

Database Setup
- Install PostgreSQL: Follow the instructions for your operating system (https://www.postgresql.org/download/).
- Create a Database: Use PostgreSQL tools (e.g., pgAdmin) to create a new database dedicated to this project.
- Schema and Queries: The project repository includes SQL files defining the database schema and any necessary queries. Execute these files within your PostgreSQL database to create the required structure.

Project Configuration
- Credentials:  Provide your PostgreSQL database connection credentials within the project's configuration (e.g., a config file or environment variables).  This includes:
  - Hostname
  - Port
  - Database Name
  - Username
  - Password

## Contributing
Feel free to fork the project and submit pull requests.

