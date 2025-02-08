from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QMessageBox)
from PySide6.QtCore import QTimer, Qt
from datetime import datetime
import yfinance as yf
from dialogs.stock_selector_dialog import StockSelectorDialog

class AddStockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Stock")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create stock selector button
        self.symbol_input = QLineEdit()
        self.symbol_input.setReadOnly(True)
        self.symbol_input.setPlaceholderText("Click 'Find Stock' to select a stock")
        self.select_stock_button = QPushButton("Find Stock")
        self.select_stock_button.clicked.connect(self.select_stock)
        layout.addWidget(self.select_stock_button)
        layout.addWidget(self.symbol_input)
        
        # Rest of the UI remains the same
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Number of shares")
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.quantity_input)
        
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Purchase price per share")
        layout.addWidget(QLabel("Purchase Price:"))
        layout.addWidget(self.price_input)
        
        self.current_price_input = QLineEdit()
        self.current_price_input.setPlaceholderText("Current price per share")
        self.current_price_input.setReadOnly(True)  # Make it read-only since it's auto-fetched
        layout.addWidget(QLabel("Current Price:"))
        layout.addWidget(self.current_price_input)
        
        # Add status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("QLabel { color: gray; }")
        layout.addWidget(self.status_label)
        
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

    def select_stock(self):
        dialog = StockSelectorDialog(self)
        if dialog.exec():
            selected_symbol = dialog.get_selected_symbol()
            print(f"Symbol selected from dialog: {selected_symbol}")  # Debug print
            if selected_symbol:
                self.symbol_input.setText(selected_symbol)
                print(f"Setting symbol input to: {selected_symbol}")  # Debug print
                QTimer.singleShot(100, self.fetch_current_price)  # Fetch price immediately after selection

    def fetch_current_price(self):
        symbol = self.symbol_input.text().strip().upper()
        print(f"Fetching price for symbol: {symbol}")  # Debug print
        if not symbol:
            self.current_price_input.clear()
            return
        
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            print(f"Got info for {symbol}: {info.keys()}")  # Debug print
            
            # Try different possible price keys
            price = None
            for price_key in ['currentPrice', 'regularMarketPrice', 'price', 'previousClose']:
                if price_key in info and info[price_key] is not None:
                    price = info[price_key]
                    break
            
            if price is None:
                self.current_price_input.clear()
                self.status_label.setText(f"Could not fetch price for {symbol}")
                self.status_label.setStyleSheet("QLabel { color: red; }")
                return
                
            self.current_price_input.setText(str(price))
            
            # Update status label with success message
            company_name = info.get('longName', symbol)
            currency = info.get('currency', 'USD')
            market_state = info.get('marketState', 'Unknown')
            
            self.status_label.setText(f"Current price: {currency} {price:.2f} ({market_state})")
            self.status_label.setStyleSheet("QLabel { color: green; }")
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error fetching price: {error_msg}")  # Debug print
            self.current_price_input.clear()
            self.status_label.setText(f"Error: {error_msg}")
            self.status_label.setStyleSheet("QLabel { color: red; }")
    
    def get_stock_data(self):
        return {
            'symbol': self.symbol_input.text().upper(),
            'quantity': int(self.quantity_input.text()),
            'purchase_price': float(self.price_input.text()),
            'current_price': float(self.current_price_input.text()),
            'date_added': datetime.now().isoformat()
        } 