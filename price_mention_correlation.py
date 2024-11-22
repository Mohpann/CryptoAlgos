import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from datetime import datetime, timedelta

def get_dogecoin_data(start_date, end_date):
    """
    Fetch Dogecoin price data using yfinance
    """
    doge = yf.download('DOGE-USD', start=start_date, end=end_date)
    return doge['Close']

def analyze_dogecoin(price_data, mention_data):
    """
    Create a dual-axis plot comparing Dogecoin price and mentions
    """
    # Create figure and axis objects with a single subplot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Dogecoin price
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('DOGE Price (USD)', color=color)
    ax1.plot(price_data.index, price_data.values, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create second y-axis that shares x-axis
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Number of Mentions', color=color)
    ax2.plot(mention_data.index, mention_data.values, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and adjust layout
    plt.title('Dogecoin Price vs Internet Mentions')
    fig.tight_layout()
    plt.grid(True, alpha=0.3)
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, ['DOGE Price', 'Mentions'], loc='upper left')
    
    return fig

def get_google_trends_data(keyword, timeframe='today 1-m'):
    """
    Fetch Google Trends data for a specific keyword
    
    Args:
    - keyword: Search term to track (e.g., 'dogecoin')
    - timeframe: Time range for data collection
    
    Returns:
    - Pandas DataFrame with interest over time
    """
    pytrends = TrendReq(hl='en-US', tz=365)
    
    # Get interest over time
    pytrends.build_payload([keyword], timeframe=timeframe)
    trends_df = pytrends.interest_over_time()
    
    return trends_df


# Example usage
if __name__ == "__main__":
    # Set date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Get Dogecoin price data
    doge_price = get_dogecoin_data(start_date, end_date)

    keyword = 'Dogecoin'
    trends_data = get_google_trends_data(keyword)

    # Fill missing data in trends_data with 0
    trends_data = trends_data.fillna(0)

    trends_data = trends_data['Dogecoin']  # Assuming 'dogecoin' is the column name for mentions
    trends_data = trends_data[2:]

    print(len(trends_data))

    print(trends_data.values)
    print(len(doge_price))
    mention_data = pd.Series(index=doge_price.index, data=trends_data.values)
    
    # Create and save the plot
    fig = analyze_dogecoin(doge_price, mention_data)
    plt.savefig('dogecoin_analysis.png')
    plt.close()