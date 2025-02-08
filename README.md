# Stock Portfolio Manager

A desktop application built with PySide6 for managing your stock portfolio. This application allows you to track your stocks, their purchase prices, and current values with real-time price updates from Yahoo Finance.

## Features

- Add stocks to your portfolio with symbol, quantity, purchase price, and current price
- Select stocks from S&P 500 list with company names
- Remove stocks from your portfolio
- Update stock prices manually or automatically from Yahoo Finance
- Fetch real-time stock prices with one click
- View total value of holdings
- Track price changes and performance (with color-coded percentage changes)
- Refresh all stock prices simultaneously
- Automatic data persistence (saves to SQLite database)
- Clean and modern user interface

## Requirements

- Python 3.10 or higher
- uv (recommended) or pip

## Quick Start

1. Install uv:

On Windows:
```bash
# Using winget (Recommended for Windows)
winget install astral.uv

# Alternative using PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Run the application:
```bash
uv run main.py
```

That's it! uv will automatically create a virtual environment and install all required dependencies.

## Development Setup

If you want to develop or modify the application, you'll need to set up a development environment:

1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows
```

2. Install the package in editable mode:
```bash
uv pip install -e .
```

3. You can now run the application using either:
```bash
python main.py
# or
uv python main.py
```

## Usage

1. **Adding a Stock**
   - Click the "Add Stock" button
   - Either:
     - Enter the stock symbol manually (e.g., AAPL), or
     - Click "Select from S&P 500" to choose from the list of S&P 500 companies
   - Enter the quantity of shares
   - Enter the purchase price per share
   - Click "Fetch Current Price" to automatically get the current market price
   - Click OK to add the stock

2. **Using the S&P 500 Stock Selector**
   - Click "Select from S&P 500" in the Add Stock dialog
   - Wait for the list to load (downloaded from Wikipedia)
   - Select a stock from the dropdown or type to search
   - Click OK to use the selected stock
   - The current price will be automatically fetched

3. **Removing a Stock**
   - Select the stock in the table
   - Click the "Remove Stock" button

4. **Updating Stock Price**
   - Select the stock in the table
   - Click the "Update Stock" button
   - Click "Fetch Current Price" to get the latest price from Yahoo Finance
   - Or manually enter the new current price
   - Click OK to update

5. **Refreshing All Prices**
   - Click the "Refresh All Prices" button to update all stock prices simultaneously
   - The application will fetch the latest prices from Yahoo Finance for all stocks in your portfolio

## Data Storage

The application stores all portfolio data in a SQLite database file (`portfolio.db`) in the same directory as the application. This file is automatically created when you first add a stock and is updated whenever you make changes to your portfolio.

## Price Updates

Stock prices are fetched from Yahoo Finance using the yfinance library. The application provides two ways to update prices:
- Individual stock updates using the "Fetch Current Price" button
- Bulk updates using the "Refresh All Prices" button

Price changes are displayed in green for gains and red for losses, making it easy to track your portfolio's performance.

## Why uv?

uv is recommended because it offers several advantages:
- Faster package installation than pip
- Better dependency resolution
- Built-in virtual environment management
- Compatible with existing Python tools
- Native binary distribution support

## Troubleshooting

If you encounter any issues:

1. Make sure you're using Python 3.10 or higher
2. Verify that your virtual environment is activated
3. Try reinstalling dependencies:
   ```bash
   uv pip install --force-reinstall -e .
   ```
4. Check that the SQLite database file has proper permissions

## Stock Selection

The application includes a built-in S&P 500 stock selector that:
- Downloads the current S&P 500 company list from Wikipedia
- Displays both stock symbols and company names
- Allows searching and filtering of stocks
- Can be refreshed to get the latest S&P 500 list
