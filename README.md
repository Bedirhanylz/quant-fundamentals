# Quantitative Trading Fundamentals

This repository documents my structured transition from discretionary trading to quantitative finance.

I am building Python-based trading tools from scratch before moving into NumPy, Pandas, vectorized backtesting, and statistical trading models.

## Current Projects

### Week 01 - Manual Stock Analyzer
Pure Python implementation of:
- Daily returns calculation
- Simple moving average calculation
- Basic moving average signal generation

### Week 02 - CSV Reader
Manual CSV reading with Python's built-in csv module:
- Reading market-style CSV files
- Extracting Close prices
- Converting string values to float
- Preparing data for analysis without pandas

### Week 02 - OOP Stock Analyzer
Object-oriented version of the stock analyzer:
- Hisse / Stock class
- Daily returns method
- Moving average method
- Signal generation method
- Reusable structure for multiple stocks

 ### Week 03 — Pandas Stock Analysis

A Pandas-based stock analysis project using historical stock price data from a CSV file.

The project calculates daily returns, moving averages, and basic BUY / SELL / WAIT signals using moving average crossover logic. It also visualizes Close price, moving averages, and signal markers with Matplotlib.

Key concepts practiced:

Pandas DataFrames
Reading CSV data with Pandas
Financial time series analysis
Daily return calculation
Rolling moving averages
Moving average crossover signals
Matplotlib visualization
Function-based project structure

### Week 04 — Simple Backtesting Project

A simple moving average crossover backtesting project using Python and Pandas.  
It includes signal generation, position tracking, shifted position logic, transaction costs, cumulative returns, and basic performance metrics.

## About

I am a discretionary trader working with US equities and futures, currently building a quantitative trading foundation through practical Python projects.
