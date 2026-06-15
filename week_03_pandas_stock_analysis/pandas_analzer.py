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
    df['Daily_Return'] = df['Close'].pct_change()

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

def main(): 
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir / "aapl.csv"
    df = csv_reader(csv_path)
    analysis_df = calculate_daily_return(df)
    analysis_df = calculate_ma(analysis_df)
    analysis_df = create_signal(analysis_df)

    print('Analyse results')
    print(analysis_df[['Date', 'Close', 'MA_20', 'MA_50', 'Signal']])
    plot_price_ma_signals(analysis_df)
    plt.show()

if __name__ == '__main__': 
    main()