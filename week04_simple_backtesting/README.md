# Week 04 — Simple Backtesting Project

## Project Overview

This project is a simple moving average crossover backtesting project built with Python and Pandas.

The main goal of this project is to understand the basic structure of a backtest, including signal generation, position tracking, strategy returns, transaction costs, cumulative returns, and performance metrics.

This is an educational project. It is not a production-ready trading system or investment advice.

---

## Features

* Reads historical stock price data from a CSV file
* Calculates daily returns
* Calculates short-term and long-term moving averages
* Generates BUY / SELL / WAIT signals using moving average crossover logic
* Converts signals into positions
* Uses shifted position logic to reduce look-ahead bias
* Calculates strategy returns
* Applies basic transaction costs
* Calculates cumulative returns
* Compares strategy performance with buy & hold
* Plots price signals and equity curves
* Calculates basic performance metrics

---

## Project Structure

```text
week_04_simple_backtesting/
    simple_backtester.py
    aapl.csv
    README.md
```

---

## Libraries Used

* pandas
* matplotlib
* pathlib

---

## Strategy Logic

The project uses a simple moving average crossover strategy.

The moving averages used are:
MA_20
MA_50


The signal logic is:

BUY  → MA_20 crosses above MA_50
SELL → MA_20 crosses below MA_50
WAIT → No crossover
Not enough data → Moving averages are not available yet

---

## Signal vs Position

One of the key concepts in this project is the difference between signal and position.

Signal   = trading event
Position = current market exposure

For example:

BUY  → enter the market
SELL → exit the market
WAIT → no new signal

A WAIT signal does not mean there is no position. It means there is no new trading signal.

## Look-Ahead Bias

In this project, the strategy uses `Shifted_Position` to avoid using the same day's signal for the same day's return.

The idea is:

Today's return should be calculated using yesterday's position.

This is handled with:

```python
df["Shifted_Position"] = df["Position"].shift(1).fillna(0)
```

Then strategy return is calculated as:

```python
df["Strategy_Return"] = df["Daily_Return"] * df["Shifted_Position"]
```

This makes the backtest logic more realistic than directly multiplying today's return by today's position.

---

## Transaction Cost

Backtests without transaction costs can be overly optimistic.

This project applies a simple transaction cost model.

A trade is detected when the shifted position changes:

```python
df["Trade"] = df["Position"].diff().abs().fillna(0)
```

Transaction cost is calculated as:

```python
df["Transaction_Cost"] = df["Trade"] * transaction_cost
```

Net strategy return is calculated as:

```python
df["Strategy_Return_After_Cost"] = df["Strategy_Return"] - df["Transaction_Cost"]
```

This allows the project to compare:

```text
Strategy return before cost
Strategy return after cost
Buy & hold return
```

---

## Calculated Metrics

The project calculates the following basic performance metrics:

* Strategy total return before cost
* Strategy total return after cost
* Market / buy & hold total return
* Average daily strategy return after cost
* Strategy volatility after cost
* Number of trades
* Days in market

These metrics are intentionally simple and are used to understand the basic behavior of the strategy.

---

## Equity Curve

The project plots cumulative returns for:

```text
Market / Buy & Hold
Strategy Before Cost
Strategy After Cost
```

The equity curve helps visualize how the strategy performs over time compared to simply buying and holding the stock.

---

## What I Learned

In this project, I practiced:

* Building a simple backtesting pipeline
* Understanding signal vs position
* Using shifted positions to reduce look-ahead bias
* Calculating strategy returns
* Applying basic transaction costs
* Calculating cumulative returns
* Comparing a strategy with buy & hold
* Creating basic performance metrics
* Structuring a Python finance project with reusable functions

---
