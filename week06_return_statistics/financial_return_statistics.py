import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt



def read_stock_data_from_csv(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df.empty:
        raise ValueError(f"The DataFrame is empty. Please check the CSV file at '{file_path}'.")    

    df = df.sort_values('Date')
    df = df.reset_index(drop=True)
    return df    

def load_close_price_series(file_path, ticker): 
    df = read_stock_data_from_csv(file_path)
    if 'Close' not in df.columns:
        raise ValueError(f"The DataFrame does not contain a 'Close' column. Please check the CSV file at '{file_path}'.")
    
    close_prices = df.set_index('Date')['Close'].rename(ticker)
    return close_prices


def calculate_simple_return(df):
    df= df.copy()
    df['Simple_Return'] = df['Close'].pct_change()
    return df

def calculate_log_return(df):
    df = df.copy()
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    return df

def calculate_return_statistics(df, return_column='Simple_Return', trading_days= 252):

    returns = df[return_column].dropna()
    if returns.empty:
        raise ValueError(f"The return column '{return_column}' is empty. Please check the data.")
    
    mean_daily_return = returns.mean()
    median_daily_return = returns.median()
    daily_variance = returns.var(ddof=1)
    daily_volatility = returns.std(ddof=1)
    annualized_volatility = daily_volatility * np.sqrt(trading_days)
    minimum_daily_return = returns.min()
    maximum_daily_return = returns.max()

    statistics = {
        'Mean Daily Return': mean_daily_return, 
        'Median Daily Return': median_daily_return,
        'Daily Variance': daily_variance,
        'Daily Volatility': daily_volatility,
        'Annualized Volatility': annualized_volatility,
        'Minimum Daily Return': minimum_daily_return,
        'Maximum Daily Return': maximum_daily_return
    }

    return statistics

def print_return_statistics(statistics):
    print('RETURN STATISTICS:')
    print('-' * 40)

    for metric_name, metric_value in statistics.items():
        if metric_name == 'Daily Variance':
            print(f'{metric_name}: {metric_value:.8f}')
        else: 
            print(f'{metric_name}: {metric_value:.2%}')

def calculate_z_score(df, return_column='Simple_Return'):
    df = df.copy()
    returns = df[return_column].dropna()

    if returns.empty:
        raise ValueError(f"The return column '{return_column}' is empty. Please check the data.")

    mean_return = returns.mean()
    std_return = returns.std(ddof=1)

    if np.isclose(std_return, 0):
        raise ValueError(f"The standard deviation of the return column '{return_column}' is zero. Z-scores cannot be calculated.")

    z_scores = (returns - mean_return) / std_return
    df['Z_Score'] = z_scores
    return df

def calculate_skewness(df, return_column='Simple_Return'):
    returns = df[return_column].dropna()
    
    if returns.empty:
        raise ValueError(f"The return column '{return_column}' is empty. Please check the data.")
    
    skewness = returns.skew()
    return skewness

def calculate_kurtosis(df, return_column='Simple_Return'):
    returns = df[return_column].dropna()
    
    if returns.empty:
        raise ValueError(f"The return column '{return_column}' is empty. Please check the data.")
    
    kurtosis = returns.kurt()
    return kurtosis

def calculate_autocorrelation(df, return_column='Simple_Return', lag=1):
    returns = df[return_column].dropna()
    
    if returns.empty:
        raise ValueError(f"The return column '{return_column}' is empty. Please check the data.")
    
    if lag < 1: 
        raise ValueError("Lag must be a positive integer.")
    
    if len(returns) <= lag:
        raise ValueError(f"The number of returns ({len(returns)}) is less than or equal to the specified lag ({lag}). Autocorrelation cannot be calculated.")
    
    
    autocorrelation = returns.autocorr(lag=lag)
    return autocorrelation

def plot_return_distribution(df, return_column='Simple_Return', bins=50):
    returns = df[return_column].dropna()
    mean_return = returns.mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(returns, bins=bins, density=True, alpha=0.6, color='b', label='Return Distribution')
    ax.axvline(mean_return, color='r', linestyle='dashed', linewidth=2, label='Mean Return')
    ax.set_title(f'{return_column} Distribution')
    ax.set_xlabel('Return')
    ax.set_ylabel('Density')
    ax.legend()
    ax.grid(alpha=0.3)


def calculate_multi_asset_returns(price_df): 
    return_df = price_df.pct_change().dropna()
    if return_df.empty:
        raise ValueError("The return DataFrame is empty after calculating percentage change. Please check the price data.")
    
    return return_df

def calculate_correlation_matrix(return_df):
    if return_df.empty:
        raise ValueError("The return DataFrame is empty. Please check the data.")
    
    correlation_matrix = return_df.corr()
    return correlation_matrix

def plot_correlation_heatmap(correlation_matrix):
    if correlation_matrix.empty:
        raise ValueError("The correlation matrix is empty. Please check the return data.")
    
    fig, ax = plt.subplots(figsize=(8, 6))

    image = ax.imshow(correlation_matrix,vmin=-1, vmax=1)

    tick_positions = range(len(correlation_matrix.columns))

    ax.set_xticks(tick_positions)
    ax.set_yticks(tick_positions)

    ax.set_xticklabels(correlation_matrix.columns)
    ax.set_yticklabels(correlation_matrix.index)

    for row_index in range(len(correlation_matrix.index)):
        for column_index in range(len(correlation_matrix.columns)):

            correlation_value = correlation_matrix.iloc[
                row_index,
                column_index
            ]

            ax.text(
                column_index,
                row_index,
                f"{correlation_value:.2f}",
                ha="center",
                va="center"
            )
    
    fig.colorbar(image, ax=ax, label='Correlation')

    ax.set_title('Daily Return Correlation Matrix')

    fig.tight_layout()


def main():
    aapl_file_path = Path(__file__).parent / 'aapl_us_d.csv'
    msft_file_path = Path(__file__).parent / 'msft_us_d.csv'
    spy_file_path = Path(__file__).parent / 'spy_us_d.csv'

    # AAPL SINGLE ASSET RETURN ANALYSIS

    aapl_df = read_stock_data_from_csv(aapl_file_path)
    aapl_df = calculate_simple_return(aapl_df)
    aapl_df = calculate_log_return(aapl_df)
    aapl_df = calculate_z_score(aapl_df, return_column='Simple_Return')
    return_statistics = calculate_return_statistics(aapl_df, return_column='Simple_Return')
    print("AAPL Return Statistics:")
    print('-' * 40)
    print(return_statistics)

    skewness = calculate_skewness(aapl_df, return_column='Simple_Return')
    kurtosis = calculate_kurtosis(aapl_df, return_column='Simple_Return')
    lag_1_autocorrelation = calculate_autocorrelation(aapl_df, return_column='Simple_Return', lag=1)
    lag_2_autocorrelation = calculate_autocorrelation(aapl_df, return_column='Simple_Return', lag=2)


    print('\n AAPL RETURN ANALYSIS:')
    print('-' * 40)
    print(f'Analysis Period:', aapl_df['Date'].min().date(), 'to', aapl_df['Date'].max().date())
    print()
    print_return_statistics(return_statistics)

    print('\nDISTRBUTION SHAPE')
    print('-' * 40)
    print(f'Skewness: {skewness:.4f}')
    print(f'Kurtosis: {kurtosis:.4f}')

    print()

    print('AUTOCORRELATION')
    print('-' * 40)
    print(f'Lag 1 Autocorrelation: {lag_1_autocorrelation:.4f}')
    print(f'Lag 2 Autocorrelation: {lag_2_autocorrelation:.4f}')

    most_extreme_days = aapl_df.loc[aapl_df['Z_Score'].abs().nlargest(5).index, ['Date', 'Close', 'Simple_Return', 'Z_Score']]
    print()

    print('MOST EXTREME DAYS BASED ON Z-SCORE:')
    print('-' * 40)
    print(most_extreme_days.to_string(index=False))


    # MULTI-ASSET RETURN ANALYSIS
    
    aapl_prices = load_close_price_series(aapl_file_path, 'AAPL')
    msft_prices = load_close_price_series(msft_file_path, 'MSFT')
    spy_prices = load_close_price_series(spy_file_path, 'SPY')

    price_df = pd.concat([aapl_prices, msft_prices, spy_prices], axis=1, join='inner').sort_index()
 

    returns_df = calculate_multi_asset_returns(price_df)
    correlation_matrix = calculate_correlation_matrix(returns_df)
    print()
    print("\nCORRELATION MATRIX:")
    print('-' * 40)
    print(f'Analysis Period: {returns_df.index.min().date()} to {returns_df.index.max().date()}')
    print(correlation_matrix)


    #VISUALIZATIONS

    plot_return_distribution(aapl_df, return_column='Simple_Return', bins=50)
    plt.show()
    
    plot_correlation_heatmap(correlation_matrix)
    plt.show()


if __name__ == '__main__': 
    main()



