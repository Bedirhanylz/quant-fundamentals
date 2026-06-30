# Financial Return Statistics Analysis

## Project Overview

This project analyzes the statistical behavior of daily stock returns using historical price data for:

* AAPL
* MSFT
* SPY

The project focuses on understanding return distributions, volatility, extreme daily movements, time-series behavior, and relationships between multiple assets.

The analysis uses daily closing prices from local CSV files and calculates both single-asset and multi-asset return metrics.

## Objectives

This project answers the following questions:

* How are AAPL daily returns distributed?
* What are the mean, median, variance, and volatility of daily returns?
* Which days had the most extreme price movements?
* Does the return distribution show skewness or fat tails?
* Does yesterday's return contain information about today's return?
* How strongly do AAPL, MSFT, and SPY move together?

## Features

### Single-Asset Return Analysis

The project calculates the following metrics for AAPL daily returns:

* Simple Return
* Log Return
* Mean Daily Return
* Median Daily Return
* Daily Variance
* Daily Volatility
* Annualized Volatility
* Minimum Daily Return
* Maximum Daily Return
* Z-Score
* Skewness
* Excess Kurtosis
* Lag 1 Autocorrelation
* Lag 2 Autocorrelation

### Distribution Analysis

The project visualizes the AAPL daily return distribution using a histogram.

It also identifies the most extreme return days based on the absolute value of the Z-score.

### Multi-Asset Correlation Analysis

The project combines AAPL, MSFT, and SPY closing prices using their common trading dates.

It then calculates:

* Daily returns for each asset
* Correlation matrix
* Correlation heatmap

## Key Concepts

### Simple Return

Simple return measures the percentage change in price between two consecutive trading days.

```text
Simple Return = Current Price / Previous Price - 1
```

Simple returns are useful for portfolio analysis, backtesting, and cumulative return calculations.

### Log Return

Log return measures the natural logarithm of the price ratio between two consecutive trading days.

```text
Log Return = ln(Current Price / Previous Price)
```

Log returns are useful in statistical analysis because they can be added across time periods.

### Volatility

Daily volatility is calculated using the sample standard deviation of daily returns.

Annualized volatility is calculated as:

```text
Annualized Volatility = Daily Volatility × √252
```

where `252` represents the approximate number of trading days in one year.

### Z-Score

Z-score measures how far a daily return is from the average return in terms of standard deviations.

```text
Z-Score = (Return - Mean Return) / Standard Deviation
```

Large positive or negative Z-scores can indicate unusually large return movements.

### Skewness

Skewness measures whether the return distribution is symmetric.

* Positive skewness may indicate stronger positive outliers.
* Negative skewness may indicate stronger negative outliers.
* Skewness close to zero suggests a more symmetric distribution.

### Excess Kurtosis

Excess kurtosis measures the presence of fat tails in the return distribution.

* Excess kurtosis near `0` is similar to a normal distribution.
* Positive excess kurtosis suggests stronger or more frequent extreme return events.

In the current AAPL analysis, the excess kurtosis was approximately `6.59`, indicating that the daily return distribution had substantially heavier tails than a normal distribution.

### Autocorrelation

Autocorrelation measures the relationship between current returns and previous returns.

```text
Lag 1 Autocorrelation
→ Relationship between today's return and yesterday's return

Lag 2 Autocorrelation
→ Relationship between today's return and the return two days ago
```

* Positive autocorrelation may suggest momentum behavior.
* Negative autocorrelation may suggest mean-reversion behavior.
* Values close to zero suggest limited linear predictive information from past returns.

### Correlation

Correlation measures the direction and strength of the linear relationship between two assets' returns.

```text
Correlation = +1
→ Perfect positive relationship

Correlation = 0
→ No linear relationship

Correlation = -1
→ Perfect negative relationship
```

High correlation does not imply causation. It only indicates that assets tend to move together during the analyzed period.


## Requirements

```text
pandas
numpy
matplotlib
```

## How to Run

Run the Python file from the project directory:

```bash
python financial_return_statistics.py
```

The script produces:

* AAPL return statistics summary
* Skewness and excess kurtosis values
* Lag 1 and Lag 2 autocorrelation values
* The most extreme AAPL return days based on Z-score
* AAPL daily return distribution histogram
* AAPL, MSFT, and SPY correlation matrix
* Correlation heatmap

## Limitations

This project is intended for educational and research purposes.

Current limitations include:

* Analysis is based on daily closing prices only.
* Only three assets are included.
* Correlation is calculated over the full sample period and is not rolling over time.
* Transaction costs, dividends, slippage, and portfolio weights are not included.
* Autocorrelation alone does not prove that a profitable trading signal exists.
* Historical statistical relationships may not remain stable in the future.

## Disclaimer

This project is for educational and research purposes only. It does not constitute investment advice.
