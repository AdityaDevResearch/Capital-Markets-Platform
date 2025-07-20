import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import yfinance as yf
import streamlit as st
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class ProfessionalAnalytics:
    """Advanced statistical and financial analytics engine"""
    
    def __init__(self):
        self.risk_free_rate = 0.05  # 5% risk-free rate assumption
    
    def calculate_stock_statistics(self, ticker: str, period: str = '1y') -> Dict:
        """Calculate comprehensive statistical metrics for a stock"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return None
            
            # Calculate returns
            returns = hist['Close'].pct_change().dropna()
            
            # Basic statistics
            stats_data = {
                'mean_return': returns.mean() * 252,  # Annualized
                'volatility': returns.std() * np.sqrt(252),  # Annualized
                'sharpe_ratio': (returns.mean() * 252 - self.risk_free_rate) / (returns.std() * np.sqrt(252)),
                'skewness': stats.skew(returns),
                'kurtosis': stats.kurtosis(returns),
                'max_drawdown': self._calculate_max_drawdown(hist['Close']),
                'var_95': np.percentile(returns, 5) * np.sqrt(252),  # 95% VaR annualized
                'var_99': np.percentile(returns, 1) * np.sqrt(252)   # 99% VaR annualized
            }
            
            return stats_data
            
        except Exception as e:
            st.error(f"Statistical analysis error for {ticker}: {str(e)}")
            return None
    
    def _calculate_max_drawdown(self, price_series: pd.Series) -> float:
        """Calculate maximum drawdown"""
        cumulative = (1 + price_series.pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def perform_regression_analysis(self, stock_ticker: str, market_ticker: str = '^GSPC', period: str = '2y') -> Dict:
        """Perform regression analysis against market benchmark"""
        try:
            # Get stock and market data
            stock = yf.Ticker(stock_ticker)
            market = yf.Ticker(market_ticker)
            
            stock_hist = stock.history(period=period)
            market_hist = market.history(period=period)
            
            if stock_hist.empty or market_hist.empty:
                return None
            
            # Align dates and calculate returns
            aligned_data = pd.merge(stock_hist['Close'], market_hist['Close'], 
                                  left_index=True, right_index=True, how='inner')
            aligned_data.columns = ['Stock', 'Market']
            
            stock_returns = aligned_data['Stock'].pct_change().dropna()
            market_returns = aligned_data['Market'].pct_change().dropna()
            
            # Perform regression
            X = market_returns.values.reshape(-1, 1)
            y = stock_returns.values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Calculate metrics
            beta = model.coef_[0]
            alpha = model.intercept_ * 252  # Annualized alpha
            r_squared = r2_score(y, model.predict(X))
            
            # Calculate correlation
            correlation = np.corrcoef(stock_returns, market_returns)[0, 1]
            
            return {
                'alpha': alpha,
                'beta': beta,
                'r_squared': r_squared,
                'correlation': correlation,
                'stock_volatility': stock_returns.std() * np.sqrt(252),
                'market_volatility': market_returns.std() * np.sqrt(252),
                'tracking_error': (stock_returns - market_returns).std() * np.sqrt(252)
            }
            
        except Exception as e:
            st.error(f"Regression analysis error: {str(e)}")
            return None
    
    def calculate_portfolio_metrics(self, tickers: List[str], weights: List[float] = None, period: str = '1y') -> Dict:
        """Calculate portfolio-level metrics"""
        try:
            if weights is None:
                weights = [1/len(tickers)] * len(tickers)  # Equal weights
            
            # Get price data for all stocks
            price_data = pd.DataFrame()
            
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                price_data[ticker] = hist['Close']
            
            # Calculate returns
            returns = price_data.pct_change().dropna()
            
            # Portfolio returns
            portfolio_returns = (returns * weights).sum(axis=1)
            
            # Calculate portfolio metrics
            portfolio_metrics = {
                'expected_return': portfolio_returns.mean() * 252,
                'volatility': portfolio_returns.std() * np.sqrt(252),
                'sharpe_ratio': (portfolio_returns.mean() * 252 - self.risk_free_rate) / (portfolio_returns.std() * np.sqrt(252)),
                'max_drawdown': self._calculate_max_drawdown(portfolio_returns.cumsum()),
                'var_95': np.percentile(portfolio_returns, 5) * np.sqrt(252),
                'correlation_matrix': returns.corr().to_dict()
            }
            
            return portfolio_metrics
            
        except Exception as e:
            st.error(f"Portfolio analysis error: {str(e)}")
            return None
    
    def monte_carlo_simulation(self, ticker: str, days: int = 252, simulations: int = 1000) -> Dict:
        """Perform Monte Carlo price simulation"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='2y')
            
            if hist.empty:
                return None
            
            # Calculate historical parameters
            returns = hist['Close'].pct_change().dropna()
            mean_return = returns.mean()
            std_return = returns.std()
            current_price = hist['Close'].iloc[-1]
            
            # Monte Carlo simulation
            simulation_results = []
            
            for _ in range(simulations):
                prices = [current_price]
                
                for _ in range(days):
                    random_return = np.random.normal(mean_return, std_return)
                    new_price = prices[-1] * (1 + random_return)
                    prices.append(new_price)
                
                simulation_results.append(prices[-1])  # Final price
            
            # Calculate statistics
            simulation_results = np.array(simulation_results)
            
            return {
                'current_price': current_price,
                'mean_final_price': simulation_results.mean(),
                'median_final_price': np.median(simulation_results),
                'percentile_5': np.percentile(simulation_results, 5),
                'percentile_25': np.percentile(simulation_results, 25),
                'percentile_75': np.percentile(simulation_results, 75),
                'percentile_95': np.percentile(simulation_results, 95),
                'probability_profit': (simulation_results > current_price).mean(),
                'expected_return': (simulation_results.mean() / current_price - 1) * 100
            }
            
        except Exception as e:
            st.error(f"Monte Carlo simulation error: {str(e)}")
            return None

# Global instance for the app
analytics_engine = ProfessionalAnalytics()

def get_stock_analytics(ticker: str):
    """Main function to get comprehensive stock analytics"""
    return analytics_engine.calculate_stock_statistics(ticker)

def get_regression_analysis(stock_ticker: str, market_ticker: str = '^GSPC'):
    """Get regression analysis results"""
    return analytics_engine.perform_regression_analysis(stock_ticker, market_ticker)

def get_monte_carlo_analysis(ticker: str, days: int = 252):
    """Get Monte Carlo simulation results"""
    return analytics_engine.monte_carlo_simulation(ticker, days)

def get_portfolio_analysis(tickers: List[str], weights: List[float] = None):
    """Get portfolio analysis"""
    return analytics_engine.calculate_portfolio_metrics(tickers, weights)
