from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QMessageBox)
import yfinance as yf

class UpdateStockDialog(QDialog):
    def __init__(self, stock_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Stock")
        self.stock_data = stock_data
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create input fields
        self.current_price_input = QLineEdit()
        self.current_price_input.setText(str(self.stock_data['current_price']))
        layout.addWidget(QLabel("Current Price:"))
        layout.addWidget(self.current_price_input)
        
        # Add fetch price button
        self.fetch_price_button = QPushButton("Fetch Current Price")
        self.fetch_price_button.clicked.connect(self.fetch_current_price)
        layout.addWidget(self.fetch_price_button)
        
        # Add buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
    
    def fetch_current_price(self):
        try:
            symbol = self.stock_data['symbol']
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Try different possible price keys
            price = None
            for price_key in ['currentPrice', 'regularMarketPrice', 'price', 'previousClose']:
                if price_key in info and info[price_key] is not None:
                    price = info[price_key]
                    break
            
            if price is None:
                QMessageBox.warning(self, "Error", f"No price data available for symbol '{symbol}'. Please verify the symbol is correct.")
                return
                
            self.current_price_input.setText(str(price))
            
            # Show additional info in a message box
            company_name = info.get('longName', symbol)
            currency = info.get('currency', 'USD')
            market_state = info.get('marketState', 'Unknown')
            
            info_msg = (f"Successfully fetched price for {company_name}\n"
                       f"Current Price: {currency} {price:.2f}\n"
                       f"Market State: {market_state}")
            QMessageBox.information(self, "Price Information", info_msg)
            
        except Exception as e:
            error_msg = str(e)
            if "regularMarketPrice" in error_msg:
                error_msg = f"Invalid symbol '{symbol}'. Please check the symbol and try again."
            QMessageBox.warning(self, "Error", f"Failed to fetch price: {error_msg}")
    
    def get_stock_data(self):
        self.stock_data['current_price'] = float(self.current_price_input.text())
        return self.stock_data 