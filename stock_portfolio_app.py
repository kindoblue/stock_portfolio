from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
import threading
from dialogs.add_stock_dialog import AddStockDialog
from dialogs.update_stock_dialog import UpdateStockDialog
from utils.stock_utils import get_current_price
from utils.db_utils import init_db, save_stock, load_stocks, update_stock, remove_stock

class StockPortfolioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Portfolio Manager")
        self.setMinimumSize(800, 600)
        
        # Initialize database
        init_db()
        
        # Initialize portfolio data
        self.portfolio = []
        self.load_portfolio()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create header
        header = QLabel("Stock Portfolio Manager")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Create buttons
        button_layout = QHBoxLayout()
        self.add_stock_button = QPushButton("Add Stock")
        self.remove_stock_button = QPushButton("Remove Stock")
        self.update_stock_button = QPushButton("Update Stock")
        self.refresh_all_button = QPushButton("Refresh All Prices")
        
        button_layout.addWidget(self.add_stock_button)
        button_layout.addWidget(self.remove_stock_button)
        button_layout.addWidget(self.update_stock_button)
        button_layout.addWidget(self.refresh_all_button)
        layout.addLayout(button_layout)
        
        # Create table
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(6)
        self.stock_table.setHorizontalHeaderLabels([
            "Symbol", "Quantity", "Purchase Price", "Current Price", "Total Value", "Change %"
        ])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.stock_table)
        
        # Connect signals
        self.add_stock_button.clicked.connect(self.add_stock)
        self.remove_stock_button.clicked.connect(self.remove_stock)
        self.update_stock_button.clicked.connect(self.update_stock)
        self.refresh_all_button.clicked.connect(self.refresh_all_prices)
        
        # Update table
        self.update_table()
    
    def refresh_all_prices(self):
        self.refresh_all_button.setEnabled(False)
        self.refresh_all_button.setText("Refreshing...")
        
        def update_prices():
            for i, stock in enumerate(self.portfolio):
                price = get_current_price(stock['symbol'])
                if price is not None:
                    stock['current_price'] = price
                    update_stock(stock, i)
            
            # Update UI in the main thread
            self.update_table()
            self.refresh_all_button.setEnabled(True)
            self.refresh_all_button.setText("Refresh All Prices")
        
        # Run the update in a separate thread
        thread = threading.Thread(target=update_prices)
        thread.start()
    
    def load_portfolio(self):
        self.portfolio = load_stocks()
    
    def update_table(self):
        self.stock_table.setRowCount(len(self.portfolio))
        for row, stock in enumerate(self.portfolio):
            self.stock_table.setItem(row, 0, QTableWidgetItem(stock['symbol']))
            self.stock_table.setItem(row, 1, QTableWidgetItem(str(stock['quantity'])))
            self.stock_table.setItem(row, 2, QTableWidgetItem(f"${stock['purchase_price']:.2f}"))
            self.stock_table.setItem(row, 3, QTableWidgetItem(f"${stock['current_price']:.2f}"))
            total_value = stock['quantity'] * stock['current_price']
            self.stock_table.setItem(row, 4, QTableWidgetItem(f"${total_value:.2f}"))
            
            # Calculate and display price change percentage
            price_change = ((stock['current_price'] - stock['purchase_price']) / stock['purchase_price']) * 100
            change_item = QTableWidgetItem(f"{price_change:.2f}%")
            change_item.setForeground(Qt.green if price_change >= 0 else Qt.red)
            self.stock_table.setItem(row, 5, change_item)
    
    def add_stock(self):
        dialog = AddStockDialog(self)
        if dialog.exec():
            stock_data = dialog.get_stock_data()
            save_stock(stock_data)
            self.portfolio.append(stock_data)
            self.update_table()
    
    def remove_stock(self):
        current_row = self.stock_table.currentRow()
        if current_row >= 0:
            if remove_stock(current_row):
                self.portfolio.pop(current_row)
                self.update_table()
    
    def update_stock(self):
        current_row = self.stock_table.currentRow()
        if current_row >= 0:
            dialog = UpdateStockDialog(self.portfolio[current_row], self)
            if dialog.exec():
                updated_stock = dialog.get_stock_data()
                if update_stock(updated_stock, current_row):
                    self.portfolio[current_row] = updated_stock
                    self.update_table() 