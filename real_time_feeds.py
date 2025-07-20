import streamlit as st
import time
from datetime import datetime
import yfinance as yf

class SimpleRealTimeData:
    """Simplified real-time data using Streamlit auto-refresh"""
    
    def __init__(self):
        self.refresh_interval = 30  # seconds
        
    def get_live_price(self, ticker):
        """Get current live price for a ticker"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d", interval="1m")
            if not data.empty:
                return {
                    'price': data['Close'].iloc[-1],
                    'change': data['Close'].iloc[-1] - data['Close'].iloc[-2],
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
        except:
            return None
    
    def add_auto_refresh(self):
        """Add auto-refresh capability to the page"""
        st.markdown("""
        <script>
        setTimeout(function(){
            window.location.reload();
        }, 30000);
        </script>
        """, unsafe_allow_html=True)
