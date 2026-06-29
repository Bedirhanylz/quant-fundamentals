import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path


def read_stock_data_from_csv(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])

    if df.empty:
        raise ValueError("The CSV file is empty.")

    df = df.sort_values('Date')
    df = df.reset_index(drop=True)

    return df

def get_stock_data_from_yahoo(ticker, start_date, end_date, csv_file_path):

    try: 
        print('Trying to read stock data from yfinance...')

        df = download_stock_data(ticker, start_date, end_date)
        print('Stock data downloaded from yfinance successfully.')
        return df

    except Exception as error:
        print('Yahoo Finance download failed. Error:', error)
        print('Trying to read stock data from CSV file...')

        df = read_stock_data_from_csv(csv_file_path)
        print('Stock data read from CSV file successfully.')
        return df


def calculate_daily_return(df): 
    df= df.copy()
    df['Daily_Return'] = df['Close'].pct_change().fillna(0)

    return df

def calculate_ma(df, short_window=20 , long_window=50): 
    df= df.copy()
    df[f'MA_{short_window}'] = df['Close'].rolling(window= short_window).mean()
    df[f'MA_{long_window}'] = df['Close'].rolling(window= long_window).mean()

    return df

def plot_price_ma_signals(df, short_window=20 , long_window=50): 
    fig, ax= plt.subplots(figsize=(15, 10))
    ax.plot(df['Date'], df['Close'], 'r--', label='Close price')
    ax.plot(df['Date'], df[f'MA_{short_window}'], 'b-' ,label='Short MA')
    ax.plot(df['Date'], df[f'MA_{long_window}'], 'm-' ,label='Long MA')

    buy_signals= df[df['Signal']=='BUY']
    sell_signals= df[df['Signal']=='SELL']

    ax.scatter(buy_signals['Date'], buy_signals['Close'], marker= '^',s=120 , linewidths= 3, edgecolors='black', label='BUY', zorder=5)

    ax.scatter(sell_signals['Date'], sell_signals['Close'], marker= 'v' ,s=120, linewidths= 3, edgecolors='black', label='SELL', zorder=5)

    ax.set_title('Close Price, MA Signals')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def create_signal(df, short_window=20 , long_window=50): 
    df = df.copy()
    signals = []

    short_column= df[f'MA_{short_window}']
    long_column= df[f'MA_{long_window}']

    for i in range(len(df)): 
        if i == 0:
            signals.append('Not enough data')
            continue

        previous_short_avg= short_column.iloc[i-1]
        current_short_avg= short_column.iloc[i]
        previous_long_avg= long_column.iloc[i-1]
        current_long_avg= long_column.iloc[i]

        if pd.isna(previous_short_avg) or pd.isna(current_short_avg) or pd.isna(previous_long_avg) or pd.isna(current_long_avg): 
            signals.append('Not enough data')
        elif previous_short_avg <= previous_long_avg and current_short_avg > current_long_avg: 
            signals.append('BUY')
        elif previous_short_avg >= previous_long_avg and current_short_avg < current_long_avg: 
            signals.append('SELL')
        else: 
            signals.append('WAIT')

    df['Signal']= signals
    return df

def calculate_position(df):
    df= df.copy()
    position = []
    current_position = 0
    for signal in df['Signal']:
        if signal == 'BUY':
            current_position = 1
        elif signal == 'SELL':
            current_position = 0
        else:
            pass
        position.append(current_position)

    df['Position'] = position
    return df

def calculate_strategy_return(df):
    df= df.copy()
    df['Shifted_Position'] = df['Position'].shift(1).fillna(0)
    df['Strategy_Return'] = df['Daily_Return'] * df['Shifted_Position'].fillna(0)
    return df

def apply_transaction_costs(df, transaction_cost=0.001):
    df = df.copy()
    df['Trade'] = df['Position'].diff().fillna(0).abs()
    df['Transaction_Cost'] = df['Trade'] * transaction_cost

    return df

def calculate_cumulative_return(df):
    df= df.copy()
    daily_returns = df['Daily_Return'].fillna(0)
    strategy_returns = df['Strategy_Return'].fillna(0)
    df['Cumulative_Market_Return'] = (1 + daily_returns).cumprod()
    df['Cumulative_Strategy_Return'] = (1 + strategy_returns).cumprod()
    df['Strategy_Return_After_Cost'] = (df['Strategy_Return'] - df['Transaction_Cost']).fillna(0)
    df['Cumulative_Strategy_Return_After_Cost'] = (1 + df['Strategy_Return_After_Cost']).cumprod()
    return df

def plot_equity_curves(df):
    fig, ax= plt.subplots(figsize=(15, 10))
    ax.plot(df['Date'], df['Cumulative_Strategy_Return_After_Cost'], 'b-', label='Cumulative Strategy Return After Cost')
    ax.plot(df['Date'], df['Cumulative_Market_Return'], 'r--', label='Cumulative Market Return')
    ax.plot(df['Date'], df['Cumulative_Strategy_Return'], 'g--', label='Cumulative Strategy Return Before Cost')
    ax.set_title('Equity Curves')
    ax.set_xlabel('Date')
    ax.set_ylabel('Portfolio Value')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def calculate_total_return(df):
    df = df.copy()
    total_return = df['Cumulative_Strategy_Return_After_Cost'].iloc[-1] - 1
    return total_return

def calculate_annualized_return(df):
    df = df.copy()
    total_return = calculate_total_return(df)
    num_days = len(df) -1
    annualized_return = (1 + total_return) ** (252 / num_days) - 1
    return annualized_return

def calculate_annualized_volatility(returns, trading_days=252):
    daily_volatility = returns.std()
    annualized_volatility = daily_volatility * (trading_days ** 0.5)
    return annualized_volatility

def market_annualized_return(df):
    df = df.copy()
    total_market_return = df['Cumulative_Market_Return'].iloc[-1] - 1
    num_days = len(df) - 1
    annualized_market_return = (1 + total_market_return) ** (252 / num_days) - 1
    return annualized_market_return

def calculate_sharpe_ratio(returns, risk_free_rate=0, trading_days=252):
    daily_risk_free_rate = risk_free_rate / trading_days
    excess_daily_returns = returns - daily_risk_free_rate
    average_excess_return = excess_daily_returns.mean()
    daily_volatility = excess_daily_returns.std()

    if daily_volatility == 0:
        return 0

    sharpe_ratio = (average_excess_return / daily_volatility) * (trading_days ** 0.5)
    return sharpe_ratio

def calculate_drawdown(equity_curve):
    equity_curve = equity_curve.copy()
    running_peak = equity_curve.cummax()
    drawdown = equity_curve / running_peak - 1
    return drawdown

def calculate_max_drawdown(drawdown_series):
    return drawdown_series.min()

def calculate_sortino_ratio(returns, risk_free_rate=0, trading_days=252):
    daily_risk_free_rate = risk_free_rate / trading_days
    excess_daily_returns = returns - daily_risk_free_rate
    average_excess_return = excess_daily_returns.mean()

    downside_returns = excess_daily_returns.clip(upper=0)
    downside_deviation = downside_returns.pow(2).mean() ** 0.5

    if downside_deviation == 0:
        return float('nan') 
    
    sortino_ratio = (average_excess_return / downside_deviation) * (trading_days ** 0.5)
    return sortino_ratio

def calculate_calmar_ratio(annualized_return, max_drawdown):
    if max_drawdown == 0:
        return float('nan') 
    calmar_ratio = annualized_return / abs(max_drawdown)
    return calmar_ratio

def calculate_trade_behavior_metrics(df):
    df = df.copy()
    strategy_return_after_cost = df['Strategy_Return_After_Cost']
    active_pnl_days = strategy_return_after_cost[strategy_return_after_cost != 0]
    positive_pnl_days = active_pnl_days[active_pnl_days > 0]
    negative_pnl_days = active_pnl_days[active_pnl_days < 0]
    win_rate = len(positive_pnl_days) / len(active_pnl_days) if len(active_pnl_days) > 0 else float('nan')
    average_winning_day = positive_pnl_days.mean() if len(positive_pnl_days) > 0 else float('nan')
    average_losing_day = negative_pnl_days.mean() if len(negative_pnl_days) > 0 else float('nan')
    number_of_trades = df['Trade'].sum()
    days_in_market = df['Shifted_Position'].sum()
    num_periods = len(df) -1
    exposure_ratio = days_in_market / num_periods if num_periods > 0 else float('nan')
    return {
        'Win Rate': win_rate,
        'Average Winning Day': average_winning_day,
        'Average Losing Day': average_losing_day,
        'Number of Trades': number_of_trades,
        'Days in Market': days_in_market,
        'Exposure Ratio': exposure_ratio
    }


def calculate_performance_summary(df):
    df = df.copy()
    strategy_return_before_cost = df['Cumulative_Strategy_Return'].iloc[-1] - 1
    strategy_return_after_cost = df['Cumulative_Strategy_Return_After_Cost'].iloc[-1] - 1
    market_total_return = df['Cumulative_Market_Return'].iloc[-1] - 1
    average_daily_return = df['Strategy_Return_After_Cost'].mean()
    annualized_return = calculate_annualized_return(df)
    annualized_market_return = market_annualized_return(df)
    strategy_volatility = df['Strategy_Return_After_Cost'].std()
    strategy_annualized_volatility = calculate_annualized_volatility(df['Strategy_Return_After_Cost'])
    annualized_volatility_market = calculate_annualized_volatility(df['Daily_Return'])
    market_sharpe_ratio = calculate_sharpe_ratio(df['Daily_Return'])
    sharpe_ratio_before_cost = calculate_sharpe_ratio(df['Strategy_Return'])
    sharpe_ratio_after_cost = calculate_sharpe_ratio(df['Strategy_Return_After_Cost'])
    market_drawdown = calculate_drawdown(df['Cumulative_Market_Return'])
    strategy_drawdown = calculate_drawdown(df['Cumulative_Strategy_Return_After_Cost'])
    max_market_drawdown = calculate_max_drawdown(market_drawdown)
    max_strategy_drawdown = calculate_max_drawdown(strategy_drawdown)
    strategy_sortino_ratio = calculate_sortino_ratio(df['Strategy_Return_After_Cost'])
    market_sortino_ratio = calculate_sortino_ratio(df['Daily_Return'])
    strategy_calmar_ratio = calculate_calmar_ratio(annualized_return, max_strategy_drawdown)
    market_calmar_ratio = calculate_calmar_ratio(annualized_market_return, max_market_drawdown)
    behavior_metrics = calculate_trade_behavior_metrics(df)
    metrics = {
        'Strategy Return Before Cost': strategy_return_before_cost,
        'Strategy Return After Cost': strategy_return_after_cost,
        'Market Total Return': market_total_return,
        'Average Daily Return': average_daily_return,
        'Annualized Market Return': annualized_market_return,
        'Annualized Return': annualized_return,
        'Volatility': strategy_volatility,
        'Annualized Volatility': strategy_annualized_volatility,
        'Market Annualized Volatility': annualized_volatility_market,
        'Market Sharpe Ratio': market_sharpe_ratio,
        'Sharpe Ratio Before Cost': sharpe_ratio_before_cost,
        'Sharpe Ratio After Cost': sharpe_ratio_after_cost,
        'Max Market Drawdown': max_market_drawdown,
        'Max Strategy Drawdown After Cost': max_strategy_drawdown,
        'Strategy Sortino Ratio': strategy_sortino_ratio,
        'Market Sortino Ratio': market_sortino_ratio,
        'Strategy Calmar Ratio': strategy_calmar_ratio,
        'Market Calmar Ratio': market_calmar_ratio,
    }
    metrics.update(behavior_metrics)
    return metrics

def print_performance_summary(summary):
    print('STRATEGY PERFORMANCE SUMMARY:')
    print('-' * 40)
    for metric_name, metric_value in summary.items():
        if ('Sharpe' in metric_name or 'Sortino' in metric_name or 'Calmar' in metric_name):
            print(f"{metric_name}: {metric_value:.4f}")
        elif 'Events' in metric_name or 'Trades' in metric_name or 'Days' in metric_name:
            print(f"{metric_name}: {metric_value:.0f}")
        else:
            print(f"{metric_name}: {metric_value:.2%}")

def main(): 
    csv_file_path = Path(__file__).parent / 'aapl_us_d.csv'
    df = get_stock_data_from_yahoo(ticker='AAPL', start_date='2015-01-01', end_date='2025-12-31', csv_file_path=csv_file_path)
    analysis_df = calculate_daily_return(df)
    analysis_df = calculate_ma(analysis_df)
    analysis_df = create_signal(analysis_df)
    analysis_df = calculate_position(analysis_df)
    analysis_df = calculate_strategy_return(analysis_df)
    analysis_df = apply_transaction_costs(analysis_df)
    analysis_df = calculate_cumulative_return(analysis_df)


    print_performance_summary(calculate_performance_summary(analysis_df))
    plot_price_ma_signals(analysis_df)
    plot_equity_curves(analysis_df)
    plt.show()

if __name__ == '__main__': 
    main()
