# Week 05 — Performance Metrics for a Moving Average Backtest

## Project Overview

This project extends a simple moving average crossover backtest by adding performance, risk, drawdown, and trade behavior metrics.

The strategy uses a long-only moving average crossover approach on AAPL daily price data. When the short moving average crosses above the long moving average, the strategy enters a long position. When the short moving average crosses below the long moving average, the strategy exits the position.

The project compares the strategy against a Buy & Hold benchmark.

## Strategy Logic

* Short moving average: 20 days
* Long moving average: 50 days
* Position type: Long only
* Entry signal: Short MA crosses above Long MA
* Exit signal: Short MA crosses below Long MA
* Transaction cost: 0.1% per transaction event
* Backtest period: AAPL daily data from 2015 to 2025

To reduce look-ahead bias, the strategy uses the previous day's position when calculating daily strategy returns.

```python
df["Shifted_Position"] = df["Position"].shift(1).fillna(0)

df["Strategy_Return"] = (
    df["Daily_Return"] * df["Shifted_Position"]
)
```

## Why Total Return Is Not Enough

Total return shows how much a strategy gained or lost over the full backtest period. However, it does not show:

* How much risk the strategy took
* How volatile the returns were
* How large the worst drawdown was
* Whether the strategy outperformed the benchmark on a risk-adjusted basis
* How often the strategy was exposed to the market

For this reason, the project calculates both return and risk metrics.

## Metrics Calculated

### Return Metrics

* Strategy Total Return Before Cost
* Strategy Total Return After Cost
* Market Total Return
* Annualized Return
* Annualized Volatility

### Risk-Adjusted Metrics

* Sharpe Ratio
* Sortino Ratio
* Calmar Ratio

### Drawdown Metrics

* Market Maximum Drawdown
* Strategy Maximum Drawdown After Cost

### Trade Behavior Metrics

* Win Rate
* Average Winning Day
* Average Losing Day
* Number of Transaction Events
* Days in Market
* Exposure


## Data Source

The project first attempts to download data using Yahoo Finance through the `yfinance` package.

If Yahoo Finance data cannot be downloaded, for example because of a rate limit, the project loads local CSV data instead.


## Current Observations

Using AAPL historical data, the moving average crossover strategy reduced volatility and maximum drawdown compared with Buy & Hold.

However, during this specific period, the Buy & Hold benchmark produced higher total return and higher risk-adjusted performance metrics.

This shows that reducing risk does not automatically mean a strategy will outperform a benchmark.

## Limitations

This is an educational backtesting project and has several limitations:

* Only one asset is tested
* Only one moving average parameter combination is used
* The strategy is long-only
* The transaction cost model is simplified
* Slippage is not included
* The strategy is not tested on out-of-sample data
* Results may differ depending on the data source and price adjustments


## Disclaimer

This project is for educational and research purposes only. It does not constitute investment advice.
