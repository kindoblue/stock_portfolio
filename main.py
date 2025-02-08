import sys
from PySide6.QtWidgets import QApplication
from stock_portfolio_app import StockPortfolioApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = StockPortfolioApp()
    window.show()
    
    sys.exit(app.exec()) 