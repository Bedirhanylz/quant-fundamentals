# Week 03 — Pandas Stock Analysis

## Project Overview

This project is a mini stock analysis tool built with Python and Pandas.

The program reads historical stock price data from a CSV file, calculates daily returns, adds moving average columns, generates basic BUY / SELL / WAIT signals using moving average crossover logic, and visualizes the result with Matplotlib.

The main purpose of this project is to practice financial time series analysis with Pandas and to build a cleaner, reusable analysis pipeline.

This project is not a full backtesting engine yet. It is a stock analysis and signal visualization tool.

---

## Features

* Reads historical stock price data from a CSV file
* Sorts the data by date
* Calculates daily returns
* Calculates short-term and long-term moving averages
* Generates BUY / SELL / WAIT signals based on moving average crossovers
* Visualizes Close price, moving averages, and signal markers
* Uses a clean function-based structure

---

## Libraries Used

* `pandas`
* `matplotlib`
* `pathlib`

---

## How It Works

The project follows a simple analysis pipeline:

```text
1. Read CSV data
2. Sort data by Date
3. Calculate daily returns
4. Add moving average columns
5. Generate trading signals
6. Plot the analysis result
```

The main script is organized with reusable functions:

```text
csv_reader()
calculate_daily_return()
calculate_ma()
create_signal()
plot_price_ma_signals()
main()
```

---

## Calculated Metrics

### Daily Return

Daily return is calculated by measuring the percentage change in the Close price from one day to the next.

```text
Daily_Return = percentage change of Close price
```

This helps analyze how much the stock moved on each trading day.

---

### Moving Averages

The project calculates two moving averages:

```text
MA_20
MA_50
```

`MA_20` represents the shorter-term trend, while `MA_50` represents the longer-term trend.

Moving averages help smooth price movements and make trend direction easier to observe.

---

## Signal Logic

The signal logic is based on moving average crossovers.

```text
BUY  → MA_20 crosses above MA_50
SELL → MA_20 crosses below MA_50
WAIT → No crossover
Not enough data → Moving average values are not available yet
```

The project does not generate a BUY or SELL signal every day. It only generates signals when a crossover happens.

---

## CSV vs Manual Data

In earlier projects, price data was manually created or handled with simpler structures.

In this project, historical stock data is read from a CSV file. This makes the analysis closer to a real financial data workflow because the data includes actual market prices, dates, and multiple rows of time series information.

Using CSV data also makes the project more scalable because the same analysis logic can be reused with different stock files.

---

## How to Run

First, make sure the CSV file is in the same folder as `pandas_analyzer.py`.

Then run:

```bash
python pandas_analyzer.py
```

The script will print the latest analysis table and display a chart with:

```text
Close price
MA_20
MA_50
BUY signals
SELL signals
```

---

## Example Output

The terminal output includes the following columns:

```text
Date
Close
Daily_Return
MA_20
MA_50
Signal
```

The chart shows the stock price, moving averages, and BUY / SELL signal markers.

---

## What I Learned

In this project, I practiced:

* Reading CSV files with Pandas
* Working with financial time series data
* Calculating daily returns
* Calculating rolling moving averages
* Creating basic crossover-based trading signals
* Visualizing financial data with Matplotlib
* Structuring Python code with reusable functions
* Separating data processing, signal generation, and plotting logic
