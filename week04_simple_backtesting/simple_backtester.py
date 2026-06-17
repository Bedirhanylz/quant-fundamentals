import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def csv_reader(file_path): 
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df= df.sort_values('Date')
    df = df.reset_index(drop=True)

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

def apply_transaction_costs(df, transaction_cost=0.01):
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
    ax.set_ylabel('Cumulative Return')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig



def calculate_performance_metrics(df):
    df = df.copy()
    strategy_return_before_cost = df['Cumulative_Strategy_Return'].iloc[-1] - 1
    final_cumulative_strategy_return = df['Cumulative_Strategy_Return_After_Cost'].iloc[-1] - 1
    final_cumulative_market_return = df['Cumulative_Market_Return'].iloc[-1] - 1
    average_daily_return = df['Strategy_Return_After_Cost'].mean()
    volatility = df['Strategy_Return_After_Cost'].std()
    number_of_trades = df['Trade'].sum()
    days_in_market = df['Shifted_Position'].sum()
    return {
        'Strategy Return Before Cost': strategy_return_before_cost,
        'Final Cumulative Strategy Return': final_cumulative_strategy_return, 
        'Final Cumulative Market Return': final_cumulative_market_return,
        'Average Daily Return': average_daily_return,
        'Volatility': volatility,
        'Number of Trades': number_of_trades,
        'Days in Market': days_in_market
    }


def main(): 
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir / "aapl.csv"
    df = csv_reader(csv_path)
    analysis_df = calculate_daily_return(df)
    analysis_df = calculate_ma(analysis_df)
    analysis_df = create_signal(analysis_df)
    analysis_df = calculate_position(analysis_df)
    analysis_df = apply_transaction_costs(analysis_df)
    analysis_df = calculate_strategy_return(analysis_df)
    analysis_df = calculate_cumulative_return(analysis_df)

    print('Analyse results')
    print('Final Performance Metrics:')
    for metric_name, metric_value in calculate_performance_metrics(analysis_df).items():
        print(f"{metric_name}: {metric_value:.5f}")
    plot_price_ma_signals(analysis_df)
    plot_equity_curves(analysis_df)
    plt.show()

if __name__ == '__main__': 
    main()
