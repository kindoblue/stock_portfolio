from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QComboBox,
                             QProgressBar)
from PySide6.QtCore import QTimer, Qt, Signal, QObject
import threading
import yfinance as yf
import pandas as pd
import requests

class StockLoader(QObject):
    progress_updated = Signal(int, str)
    loading_finished = Signal(list)
    
    def __init__(self):
        super().__init__()
        
    def load_stocks(self):
        try:
            self.progress_updated.emit(0, "Downloading S&P 500 list...")
            
            try:
                # Try to get the S&P 500 list from Wikipedia
                url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
                tables = pd.read_html(url)
                df = tables[0]
                
                # Clean up symbols and get the list
                df['Symbol'] = df['Symbol'].str.replace('.', '-')
                stocks = [(symbol.strip(), security.strip()) 
                         for symbol, security in zip(df['Symbol'], df['Security'])]
                
                self.progress_updated.emit(10, f"Found {len(stocks)} S&P 500 stocks")
                
            except Exception as e:
                print(f"Error downloading S&P 500 list: {str(e)}")
                self.progress_updated.emit(5, "Using backup stock list...")
                # Use the predefined list as backup
                stocks = [
                    ("AAPL", "Apple Inc."),
                    ("MSFT", "Microsoft Corporation"),
                    ("GOOGL", "Alphabet Inc."),
                    ("AMZN", "Amazon.com Inc."),
                    ("META", "Meta Platforms Inc."),
                    ("NVDA", "NVIDIA Corporation"),
                    ("BRK-B", "Berkshire Hathaway Inc."),
                    ("JPM", "JPMorgan Chase & Co."),
                    ("JNJ", "Johnson & Johnson"),
                    ("V", "Visa Inc."),
                    ("PG", "Procter & Gamble Company"),
                    ("XOM", "Exxon Mobil Corporation"),
                    ("WMT", "Walmart Inc."),
                    ("MA", "Mastercard Incorporated"),
                    ("CVX", "Chevron Corporation"),
                    ("HD", "The Home Depot Inc."),
                    ("BAC", "Bank of America Corporation"),
                    ("KO", "The Coca-Cola Company"),
                    ("PFE", "Pfizer Inc."),
                    ("ABBV", "AbbVie Inc."),
                    ("UNH", "UnitedHealth Group Inc."),
                    ("LLY", "Eli Lilly and Company"),
                    ("AVGO", "Broadcom Inc."),
                    ("TSM", "Taiwan Semiconductor Manufacturing"),
                    ("COST", "Costco Wholesale Corporation"),
                    ("TMO", "Thermo Fisher Scientific"),
                    ("MRK", "Merck & Co."),
                    ("CSCO", "Cisco Systems Inc."),
                    ("ACN", "Accenture plc"),
                    ("ADBE", "Adobe Inc."),
                    ("MCD", "McDonald's Corporation"),
                    ("ABT", "Abbott Laboratories"),
                    ("DHR", "Danaher Corporation"),
                    ("NEE", "NextEra Energy Inc."),
                    ("DIS", "The Walt Disney Company"),
                    ("IBM", "International Business Machines"),
                    ("INTC", "Intel Corporation"),
                    ("QCOM", "QUALCOMM Incorporated"),
                    ("AMD", "Advanced Micro Devices Inc."),
                    ("INTU", "Intuit Inc.")
                ]
            
            total_stocks = len(stocks)
            self.progress_updated.emit(10, "Verifying stock information...")
            
            # Try to get company names from yfinance for any missing ones
            for i, (symbol, name) in enumerate(stocks):
                progress = int(10 + (i / total_stocks * 90))
                self.progress_updated.emit(progress, f"Loading info for {symbol}...")
                
                if name == symbol:
                    try:
                        stock = yf.Ticker(symbol)
                        new_name = stock.info.get('longName')
                        if new_name:
                            stocks[i] = (symbol, new_name)
                    except Exception as e:
                        print(f"Error fetching info for {symbol}: {str(e)}")
            
            stocks.sort(key=lambda x: x[0])
            self.progress_updated.emit(100, "Stock loading complete!")
            self.loading_finished.emit(stocks)
            
        except Exception as e:
            print(f"Error loading stocks: {str(e)}")
            self.progress_updated.emit(100, "Error loading stocks. Using fallback list.")
            self.loading_finished.emit([
                ("AAPL", "Apple Inc."),
                ("MSFT", "Microsoft Corporation"),
                ("GOOGL", "Alphabet Inc."),
            ])

class StockSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Selector")
        self.setMinimumSize(400, 150)
        self.selected_symbol = None
        self.sp500_stocks = []
        
        # Create stock loader
        self.loader = StockLoader()
        self.loader.progress_updated.connect(self._update_progress_ui)
        self.loader.loading_finished.connect(self._on_loading_finished)
        
        self.setup_ui()
        print("StockSelectorDialog initialized")
        
        # Start loading stocks immediately
        self.load_sp500_stocks()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add search field
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search stocks...")
        self.search_input.textChanged.connect(self.filter_stocks)
        self.search_input.setEnabled(False)  # Initially disabled
        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        
        # Add combobox for stock selection
        self.stock_combo = QComboBox()
        self.stock_combo.setEditable(False)
        self.stock_combo.setPlaceholderText("Loading stocks...")
        self.stock_combo.setEnabled(False)  # Initially disabled
        self.stock_combo.currentIndexChanged.connect(self.on_selection_changed)
        self.select_label = QLabel("Select Stock:")
        self.select_label.setEnabled(False)  # Initially disabled
        layout.addWidget(self.select_label)
        layout.addWidget(self.stock_combo)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Loading stocks... %p%")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)
        
        # Add status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Add buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)  # Disable until selection is made
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        print("UI setup complete")  # Debug print

    def on_selection_changed(self, index):
        self.ok_button.setEnabled(index >= 0)
        if index >= 0:
            self.selected_symbol = self.stock_combo.itemData(index)
            print(f"Selected symbol: {self.selected_symbol}")  # Debug print

    def _update_progress_ui(self, value, status):
        print(f"Setting progress bar value: {value}")
        self.progress_bar.setValue(value)
        if status:
            self.status_label.setText(status)

    def load_sp500_stocks(self):
        print("Starting stock loading process")
        
        def start_loading():
            thread = threading.Thread(target=self.loader.load_stocks)
            thread.daemon = True
            thread.start()
            print("Loading thread started")
        
        # Start loading immediately
        start_loading()

    def _on_loading_finished(self, stocks):
        print("Loading finished")
        self.sp500_stocks = stocks
        self._update_ui_after_load()

    def _update_ui_after_load(self):
        """Update UI components after stocks are loaded"""
        print("Updating UI after load")  # Debug print
        if len(self.sp500_stocks) > 0:
            self.update_combo_box()
            self.stock_combo.setEnabled(True)
            self.select_label.setEnabled(True)
            self.search_input.setEnabled(True)
            self.stock_combo.setPlaceholderText("Select a stock")
            self.progress_bar.hide()
            self.status_label.setText(f"Loaded {len(self.sp500_stocks)} stocks")
            print(f"Stock selection enabled with {len(self.sp500_stocks)} stocks")
        else:
            self.stock_combo.setPlaceholderText("No stocks available")
            self.status_label.setText("Failed to load stocks")
            print("No stocks were loaded")

    def filter_stocks(self, search_text):
        if not search_text:
            self.update_combo_box()
            return
        
        filtered_stocks = [
            (symbol, name) for symbol, name in self.sp500_stocks
            if search_text.lower() in symbol.lower() or search_text.lower() in name.lower()
        ]
        
        self.stock_combo.clear()
        for symbol, name in filtered_stocks:
            self.stock_combo.addItem(f"{symbol} - {name}", symbol)
        
        # Automatically select the first matching item if available
        if filtered_stocks:
            self.stock_combo.setCurrentIndex(0)
            # Update the selected symbol
            self.selected_symbol = filtered_stocks[0][0]
            print(f"Auto-selected symbol: {self.selected_symbol}")
        else:
            self.selected_symbol = None
            self.ok_button.setEnabled(False)

    def update_combo_box(self):
        self.stock_combo.clear()
        for symbol, name in self.sp500_stocks:
            self.stock_combo.addItem(f"{symbol} - {name}", symbol)

    def get_selected_symbol(self):
        return self.selected_symbol 