# Moving Average Parameter Research

This project evaluates different moving average crossover parameter combinations for a long-only trading strategy using historical AAPL daily price data.

The purpose is not only to identify the parameter set with the highest historical return, but also to compare strategy performance through risk-adjusted metrics and validate the selected parameters on unseen data.

## Project Objectives

* Generate valid short and long moving average combinations
* Run a moving average crossover backtest for each parameter set
* Compare Total Return, Sharpe Ratio, and Maximum Drawdown
* Visualize parameter performance using heatmaps
* Select the best parameter set based on Sharpe Ratio and a drawdown constraint
* Separate historical data into in-sample and out-of-sample periods
* Evaluate whether the selected parameter set remains effective on unseen data

## Strategy Logic

The strategy uses two moving averages:

* **Short Moving Average:** Faster trend indicator
* **Long Moving Average:** Slower trend indicator

Trading rules:

* Buy when the short moving average is above the long moving average
* Sell when the short moving average falls below the long moving average
* Apply transaction costs when the position changes
* Use the previous day's position when calculating strategy returns to avoid look-ahead bias

## Parameter Grid

The project tests the following moving average windows:

```python
short_windows = [10, 20, 50]
long_windows = [30, 50, 100, 200]
```

Only valid parameter combinations are tested:

```python
short_window < long_window
```

Example valid pairs:

```text
10 / 30
10 / 50
10 / 100
20 / 50
50 / 200
```

## Performance Metrics

### Total Return

Measures the total cumulative return of the strategy.

```text
Total Return = Final Equity Curve Value - 1
```

### Sharpe Ratio

Measures return relative to volatility.

A higher Sharpe Ratio generally indicates a more efficient risk-adjusted return profile.

### Maximum Drawdown

Measures the largest peak-to-trough decline in the strategy equity curve.

```text
More negative Maximum Drawdown
→ Larger historical loss from a previous peak
```

## Parameter Selection

The project can select the best parameter set using a chosen metric.

Example:

```python
best_parameter = find_best_parameter_set(
    in_sample_results_df,
    metric="Sharpe_Ratio",
    max_drawdown_limit=-0.30
)
```

This means:

1. Remove strategies with a drawdown worse than -30%
2. Rank the remaining strategies by Sharpe Ratio
3. Select the strategy with the highest Sharpe Ratio

## Heatmaps

The project creates heatmaps for:

* Sharpe Ratio
* Total Return

Heatmap structure:

```text
X-axis → Long MA Window
Y-axis → Short MA Window
Color → Performance metric
```

Heatmaps help evaluate whether strong performance is concentrated around a stable parameter region or only appears in a single isolated parameter combination.

## In-Sample and Out-of-Sample Testing

Historical data is divided into two periods:

```text
In-Sample Period
→ Used for parameter research and parameter selection

Out-of-Sample Period
→ Used to evaluate the selected parameters on unseen data
```

Important rule:

```text
Parameters are selected only using in-sample data.

Out-of-sample data is not used to search for a new best parameter.
```

This helps reduce the risk of overfitting.

## Overfitting Risk

A parameter set can look excellent in historical data because it fits the specific behavior of that period rather than because it captures a persistent market edge.

Example:

```text
High in-sample Sharpe Ratio
Low or negative out-of-sample Sharpe Ratio
→ Possible overfitting or market regime change
```

A more robust strategy is expected to show reasonably consistent behavior across both periods, even if out-of-sample performance is weaker.

## Installation

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Running the Project

Run the Python file from the project folder:

```bash
python parameter_testing.py
```

The program will:

1. Load AAPL daily price data
2. Split data into in-sample and out-of-sample periods
3. Test all valid moving average combinations on the in-sample period
4. Compare Total Return, Sharpe Ratio, and Maximum Drawdown
5. Generate Sharpe Ratio and Total Return heatmaps
6. Select the best in-sample parameter set
7. Test the selected parameters on the out-of-sample period
8. Display an in-sample versus out-of-sample performance comparison

## Disclaimer

This project is for educational and research purposes only. Historical backtest results do not guarantee future performance.
