import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
import tkinter as tk
from functools import partial


def refresh_portfolio(assets, units, prices):
    new_prices = []
    for asset in assets:
        symbol = get_symbol(asset)
        if symbol:
            price = fetch_price(symbol)
            if price is not None:
                new_prices.append(price)
            else:
                print(f"Failed to fetch price for {asset}.")
                new_prices.append(prices[assets.index(asset)])
        else:
            new_prices.append(prices[assets.index(asset)])

    total_value = sum(units[i] * new_prices[i] for i in range(len(units)))
    print(f"Total portfolio value: ${total_value:.2f}")
    percentages = [(units[i] * new_prices[i] / total_value) * 100 for i in range(len(units))]

    labels = [f"{assets[i]}: {percentages[i]:.2f}%" for i in range(len(units))]

    colors = []
    for stock in assets:
        if stock == 'bitcoin':
            colors.append('#FFA500')  # Orange
        elif stock == 'cash':
            colors.append('#32CD32')  # Green
        elif stock == 'solana':
            colors.append('#9370DB')  # Light blue
        elif stock == 'meme':
            colors.append('#FF6347')  # Tomato TODO rename to 'high risk trading'
        else:
            colors.append('#333333')  # Grey = unknown asset

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('#F0F0F0')
    ax.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title('Portfolio Composition')
    plt.show()


def fetch_price(symbol):
    api_key = 'XDF1s9HY6A7a2jAHKYm7rn7HUOBlmWuLr8RvfOKMJxLJXeiGX18iVBlN5H9qEPIm'
    symbol = symbol.upper()

    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT'
    response = requests.get(url, headers={'X-MBX-APIKEY': api_key})
    if response.status_code == 200:
        data = response.json()
        price = float(data['price'])
        return price
    else:
        print('Failed to fetch price:', response.text)
        return None


def get_symbol(name):
    name = name.lower()
    symbol_map = {
        'bitcoin': 'BTC',
        'solana': 'SOL',
        # add mappings as needed
    }
    return symbol_map.get(name)


def create_pie_chart(assets, units, prices):
    total_value = sum(units[i] * prices[i] for i in range(len(units)))
    print(f"Total portfolio value: ${total_value:.2f}")
    percentages = [(units[i] * prices[i] / total_value) * 100 for i in range(len(units))]

    labels = [f"{assets[i]}: {percentages[i]:.2f}%" for i in range(len(units))]

    # define colours for assets as needed
    colors = []
    for stock in assets:
        if stock == 'bitcoin':
            colors.append('#FFA500')  # Orange
        elif stock == 'cash':
            colors.append('#32CD32')  # Green
        elif stock == 'solana':
            colors.append('#9370DB')  # Light blue
        elif stock == 'meme':
            colors.append('#FF6347')  # Tomato TODO rename to 'high risk trading'
        else:
            # Choose a complementary color that won't clash
            colors.append('#333333')  # Grey = unknown asset

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('#F0F0F0')
    ax.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.set_title('Portfolio Composition')
    plt.show()


def save_portfolio(stocks, units, prices):
    with open('portfolio.txt', 'w') as f:
        for stock, unit, price in zip(stocks, units, prices):
            f.write(f"{stock},{unit},{price}\n")


def load_portfolio():
    if os.path.exists('portfolio.txt'):
        stocks, units, prices = [], [], []
        with open('portfolio.txt', 'r') as f:
            for line in f:
                stock, unit, price = line.strip().split(',')
                stocks.append(stock)
                units.append(float(unit))
                prices.append(float(price))
        return stocks, units, prices
    else:
        return [], [], []


def main():
    choice = input("Do you want to load previous portfolio data? (y/n): ").lower()
    if choice == 'y':
        assets, units, prices = load_portfolio()
    else:
        assets, units, prices = [], [], []
        num_stocks = int(input("Enter the number of assets in your portfolio: "))

        for i in range(num_stocks):
            asset = input(f"Enter the name of stock/crypto {i + 1}: ")
            symbol = get_symbol(asset)
            if symbol:
                assets.append(asset)
                unit = float(input(f"Enter the number of units of {asset}: "))
                units.append(unit)
                price = fetch_price(symbol)
                if price is not None:
                    prices.append(price)
                else:
                    print(f"Symbol found for {asset}, but failed to fetch price.")
                    price = float(input(f"Enter the current price of {asset}: "))
                    prices.append(price)
            else:
                print(f"Symbol not found for {asset}.")
                price = float(input(f"Enter the current price of {asset}: "))
                assets.append(asset)
                units.append(float(input(f"Enter the number of units of {asset}: ")))
                prices.append(price)

    save_portfolio(assets, units, prices)

    df = pd.DataFrame({'Asset': assets, 'Units': units, 'Price': prices})
    print("\nPortfolio Summary:")
    print(df)

    create_pie_chart(assets, units, prices)
    # Create a Tkinter window and a refresh button
    root = tk.Tk()
    refresh_button = tk.Button(root, text="Refresh Portfolio", command=partial(refresh_portfolio, assets, units, prices))
    refresh_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

# selling about 0.005 Btc at a time
# refresh button that resets pf pricings - part of menu system --