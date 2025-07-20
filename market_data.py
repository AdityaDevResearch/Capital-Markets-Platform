import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from typing import Dict, List, Tuple
import requests
from bs4 import BeautifulSoup

class RealTimeMarketIntelligence:
    """Professional-grade real-time market data and analytics engine"""
    
    def __init__(self):
        self.major_indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'Dow Jones': '^DJI',
            'Russell 2000': '^RUT',
            'FTSE 100': '^FTSE',
            'Nikkei 225': '^N225',
            'Nifty 50': '^NSEI',
            'Sensex': '^BSESN'
        }
        
        self.sector_etfs = {
            'Technology': 'XLK',
            'Financial': 'XLF',
            'Healthcare': 'XLV',
            'Energy': 'XLE',
            'Consumer Discretionary': 'XLY',
            'Industrials': 'XLI',
            'Materials': 'XLB',
            'Utilities': 'XLU'
        }
    
    @st.cache_data(ttl=30)  # Cache for 30 seconds
    def get_live_market_overview(self) -> Dict:
        """Get comprehensive real-time market overview"""
        try:
            market_data = {}
            
            # Get major indices
            for name, symbol in self.major_indices.items():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d', interval='1m')
                info = ticker.info
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = info.get('previousClose', current_price)
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100
                    
                    market_data[name] = {
                        'symbol': symbol,
                        'price': current_price,
                        'change': change,
                        'change_percent': change_percent,
                        'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0,
                        'last_updated': datetime.now()
                    }
            
            return market_data
            
        except Exception as e:
            st.error(f"Market data retrieval error: {str(e)}")
            return {}
    
    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_top_movers(self, market='US') -> Dict:
        """Get top gaining and losing stocks"""
        try:
            if market == 'US':
                # Get S&P 500 components (simplified list)
                sp500_tickers = [
                    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B',
                    'UNH', 'JNJ', 'XOM', 'JPM', 'V', 'PG', 'MA', 'HD', 'CVX', 'ABBV',
                    'PFE', 'KO', 'AVGO', 'COST', 'DIS', 'ADBE', 'WMT', 'BAC', 'TMO',
                    'CRM', 'ACN', 'VZ', 'NFLX', 'CMCSA', 'ABT', 'NKE', 'LLY', 'ORCL'
                ]
            else:  # Indian market
                sp500_tickers = [
                    'TCS.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
                    'SBIN.NS', 'BHARTIARTL.NS', 'HCLTECH.NS', 'ITC.NS', 'KOTAKBANK.NS',
                    'LT.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS',
                    'WIPRO.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'BAJFINANCE.NS', 'TITAN.NS'
                ]
            
            movers_data = {'gainers': [], 'losers': []}
            
            for ticker in sp500_tickers[:20]:  # Analyze top 20 to avoid rate limits
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period='2d')
                    info = stock.info
                    
                    if len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        previous_close = hist['Close'].iloc[-2]
                        change_percent = ((current_price - previous_close) / previous_close) * 100
                        
                        stock_data = {
                            'ticker': ticker,
                            'name': info.get('shortName', ticker),
                            'price': current_price,
                            'change_percent': change_percent,
                            'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                        }
                        
                        if change_percent > 0:
                            movers_data['gainers'].append(stock_data)
                        else:
                            movers_data['losers'].append(stock_data)
                            
                except Exception:
                    continue
            
            # Sort and return top 5 of each
            movers_data['gainers'] = sorted(movers_data['gainers'], 
                                          key=lambda x: x['change_percent'], reverse=True)[:5]
            movers_data['losers'] = sorted(movers_data['losers'], 
                                         key=lambda x: x['change_percent'])[:5]
            
            return movers_data
            
        except Exception as e:
            st.error(f"Top movers data error: {str(e)}")
            return {'gainers': [], 'losers': []}
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_sector_performance(self) -> Dict:
        """Get sector performance data"""
        try:
            sector_data = {}
            
            for sector, etf in self.sector_etfs.items():
                try:
                    ticker = yf.Ticker(etf)
                    hist = ticker.history(period='5d')
                    
                    if len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        previous_close = hist['Close'].iloc[0]
                        change_percent = ((current_price - previous_close) / previous_close) * 100
                        
                        sector_data[sector] = {
                            'etf': etf,
                            'price': current_price,
                            'change_percent': change_percent,
                            'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                        }
                        
                except Exception:
                    continue
            
            return sector_data
            
        except Exception as e:
            st.error(f"Sector performance data error: {str(e)}")
            return {}
    
    def get_market_sentiment(self) -> Dict:
        """Calculate overall market sentiment score"""
        try:
            # Get VIX (Fear & Greed Index)
            vix = yf.Ticker('^VIX')
            vix_hist = vix.history(period='2d')
            
            if not vix_hist.empty:
                vix_current = vix_hist['Close'].iloc[-1]
                
                # Calculate sentiment based on VIX levels
                if vix_current < 15:
                    sentiment = "Extremely Bullish"
                    score = 85
                elif vix_current < 20:
                    sentiment = "Bullish"
                    score = 70
                elif vix_current < 25:
                    sentiment = "Neutral"
                    score = 50
                elif vix_current < 30:
                    sentiment = "Bearish"
                    score = 30
                else:
                    sentiment = "Extremely Bearish"
                    score = 15
                
                return {
                    'sentiment': sentiment,
                    'score': score,
                    'vix_level': vix_current,
                    'last_updated': datetime.now()
                }
            
            return {'sentiment': 'Neutral', 'score': 50, 'vix_level': 20}
            
        except Exception:
            return {'sentiment': 'Neutral', 'score': 50, 'vix_level': 20}

# Global instance for the app
market_intelligence = RealTimeMarketIntelligence()

def get_live_market_data():
    """Main function to get live market data"""
    return market_intelligence.get_live_market_overview()

def get_market_movers(market='US'):
    """Get top gainers and losers"""
    return market_intelligence.get_top_movers(market)

def get_sector_data():
    """Get sector performance"""
    return market_intelligence.get_sector_performance()

def get_sentiment_data():
    """Get market sentiment"""
    return market_intelligence.get_market_sentiment()
