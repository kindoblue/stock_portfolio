import sqlite3
from datetime import datetime
from pathlib import Path

def get_db_path():
    """Get the path to the SQLite database file."""
    return Path('portfolio.db')

def init_db():
    """Initialize the database with the required table."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Create stocks table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            current_price REAL NOT NULL,
            date_added TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_stock(stock_data):
    """Save a new stock to the database."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO stocks (symbol, quantity, purchase_price, current_price, date_added)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        stock_data['symbol'],
        stock_data['quantity'],
        stock_data['purchase_price'],
        stock_data['current_price'],
        stock_data.get('date_added', datetime.now().isoformat())
    ))
    
    conn.commit()
    conn.close()

def load_stocks():
    """Load all stocks from the database."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    cursor.execute('SELECT symbol, quantity, purchase_price, current_price, date_added FROM stocks')
    rows = cursor.fetchall()
    
    stocks = []
    for row in rows:
        stocks.append({
            'symbol': row[0],
            'quantity': row[1],
            'purchase_price': row[2],
            'current_price': row[3],
            'date_added': row[4]
        })
    
    conn.close()
    return stocks

def update_stock(stock_data, index):
    """Update a stock in the database by its index."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Get the ID of the stock at the given index
    cursor.execute('SELECT id FROM stocks LIMIT 1 OFFSET ?', (index,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return False
    
    stock_id = result[0]
    
    cursor.execute('''
        UPDATE stocks 
        SET current_price = ?
        WHERE id = ?
    ''', (stock_data['current_price'], stock_id))
    
    conn.commit()
    conn.close()
    return True

def remove_stock(index):
    """Remove a stock from the database by its index."""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Get the ID of the stock at the given index
    cursor.execute('SELECT id FROM stocks LIMIT 1 OFFSET ?', (index,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return False
    
    stock_id = result[0]
    
    cursor.execute('DELETE FROM stocks WHERE id = ?', (stock_id,))
    
    conn.commit()
    conn.close()
    return True 