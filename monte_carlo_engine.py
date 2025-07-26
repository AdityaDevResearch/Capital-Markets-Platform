import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Tuple

class MonteCarloRiskEngine:
    def __init__(self):
        self.simulations = 10000
        self.trading_days = 252
        
    @st.cache_data
    def fetch_portfolio_data(_self, tickers: List[str], period: str = "2y"):
        """Fetch historical data for portfolio securities"""
        try:
            data = {}
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    data[ticker] = hist['Close'].dropna()
            return data
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return {}
    
    def calculate_returns(self, price_data: Dict) -> pd.DataFrame:
        """Calculate daily returns for all securities"""
        returns_data = {}
        for ticker, prices in price_data.items():
            returns_data[ticker] = prices.pct_change().dropna()
        
        return pd.DataFrame(returns_data)
    
    def portfolio_monte_carlo(self, tickers: List[str], weights: List[float], 
                            days_ahead: int = 252) -> Dict:
        """Run Monte Carlo simulation for portfolio"""
        
        # Fetch historical data
        price_data = self.fetch_portfolio_data(tickers)
        if not price_data:
            return {}
            
        # Calculate returns
        returns_df = self.calculate_returns(price_data)
        
        # Ensure we have data for all tickers
        common_tickers = [t for t in tickers if t in returns_df.columns]
        if len(common_tickers) != len(tickers):
            st.warning(f"Data unavailable for some tickers. Using: {common_tickers}")
        
        returns_df = returns_df[common_tickers]
        weights = np.array(weights[:len(common_tickers)])
        weights = weights / weights.sum()  # Normalize weights
        
        # Portfolio statistics
        portfolio_returns = (returns_df * weights).sum(axis=1)
        mean_return = portfolio_returns.mean()
        std_return = portfolio_returns.std()
        
        # Monte Carlo simulation
        simulated_returns = np.random.normal(
            mean_return, std_return, (self.simulations, days_ahead)
        )
        
        # Calculate cumulative returns
        cumulative_returns = np.cumprod(1 + simulated_returns, axis=1)
        final_returns = cumulative_returns[:, -1] - 1
        
        # Risk metrics
        var_95 = np.percentile(final_returns, 5)
        var_99 = np.percentile(final_returns, 1)
        expected_return = np.mean(final_returns)
        volatility = np.std(final_returns)
        
        # Sharpe ratio (assuming 2% risk-free rate)
        risk_free_rate = 0.02
        sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Maximum drawdown simulation
        portfolio_paths = np.cumprod(1 + simulated_returns, axis=1)
        running_max = np.maximum.accumulate(portfolio_paths, axis=1)
        drawdowns = (portfolio_paths - running_max) / running_max
        max_drawdown = np.min(drawdowns, axis=1)
        avg_max_drawdown = np.mean(max_drawdown)
        
        return {
            'expected_return': expected_return,
            'volatility': volatility,
            'var_95': var_95,
            'var_99': var_99,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': avg_max_drawdown,
            'simulation_paths': cumulative_returns[:100],  # Store 100 paths for plotting
            'final_returns_distribution': final_returns,
            'portfolio_returns_historical': portfolio_returns,
            'correlation_matrix': returns_df.corr(),
            'individual_volatilities': returns_df.std(),
            'tickers': common_tickers,
            'weights': weights
        }
    
    def risk_contribution_analysis(self, results: Dict) -> Dict:
        """Calculate risk contribution of each security"""
        if not results:
            return {}
            
        correlation_matrix = results['correlation_matrix']
        weights = results['weights']
        volatilities = results['individual_volatilities']
        
        # Portfolio variance
        portfolio_variance = np.dot(weights, np.dot(correlation_matrix * np.outer(volatilities, volatilities), weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Marginal risk contribution
        marginal_contrib = np.dot(correlation_matrix * np.outer(volatilities, volatilities), weights) / portfolio_volatility
        
        # Component risk contribution
        risk_contrib = weights * marginal_contrib
        risk_contrib_pct = risk_contrib / portfolio_volatility
        
        return {
            'marginal_contribution': marginal_contrib,
            'risk_contribution': risk_contrib,
            'risk_contribution_pct': risk_contrib_pct,
            'portfolio_volatility': portfolio_volatility
        }

