import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import scipy.optimize as sco
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AdvancedPortfolioAnalyzer:
    """Professional-grade portfolio analysis with institutional features"""
    
    def __init__(self, tickers, weights=None):
        self.tickers = tickers
        self.weights = weights if weights else [1/len(tickers)] * len(tickers)
        self.data = {}
        self.returns_df = None
        self.correlation_matrix = None
        
    def fetch_portfolio_data(self, period="1y"):
        """Fetch comprehensive data for all portfolio securities"""
        data_dict = {}
        
        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period=period)
                
                if not hist.empty:
                    data_dict[ticker] = {
                        'name': info.get('longName', ticker),
                        'sector': info.get('sector', 'Unknown'),
                        'price': info.get('currentPrice', hist['Close'][-1]),
                        'market_cap': info.get('marketCap', 0),
                        'pe_ratio': info.get('trailingPE', 0),
                        'beta': info.get('beta', 1.0),
                        'historical_prices': hist['Close'],
                        'volume': hist['Volume'].mean()
                    }
            except Exception as e:
                st.warning(f"Could not fetch data for {ticker}: {str(e)}")
                
        self.data = data_dict
        return data_dict
    
    def calculate_returns_matrix(self):
        """Calculate returns matrix for portfolio optimization"""
        if not self.data:
            return None
            
        price_data = {}
        for ticker, data in self.data.items():
            if 'historical_prices' in data:
                price_data[ticker] = data['historical_prices']
        
        if not price_data:
            return None
            
        prices_df = pd.DataFrame(price_data).dropna()
        returns_df = prices_df.pct_change().dropna()
        
        self.returns_df = returns_df
        self.correlation_matrix = returns_df.corr()
        
        return returns_df
    
    def calculate_portfolio_metrics(self):
        """Calculate comprehensive portfolio performance metrics"""
        if self.returns_df is None:
            return None
            
        # Portfolio returns
        portfolio_returns = (self.returns_df * self.weights).sum(axis=1)
        
        # Risk metrics
        annual_return = portfolio_returns.mean() * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility != 0 else 0
        
        # VaR calculations
        var_95 = np.percentile(portfolio_returns, 5)
        var_99 = np.percentile(portfolio_returns, 1)
        
        # Maximum drawdown
        cumulative_returns = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        return {
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'var_95': var_95,
            'var_99': var_99,
            'max_drawdown': max_drawdown,
            'portfolio_returns': portfolio_returns
        }
    
    def optimize_portfolio(self, target='sharpe'):
        """Optimize portfolio weights using Modern Portfolio Theory"""
        if self.returns_df is None or len(self.returns_df.columns) < 2:
            return None
            
        returns = self.returns_df.mean() * 252
        cov_matrix = self.returns_df.cov() * 252
        
        def portfolio_stats(weights):
            portfolio_return = np.sum(returns * weights)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe = portfolio_return / portfolio_volatility
            return portfolio_return, portfolio_volatility, sharpe
        
        def minimize_volatility(weights):
            return portfolio_stats(weights)[1]
        
        def negative_sharpe(weights):
            return -portfolio_stats(weights)[2]
        
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(len(self.tickers)))
        
        # Equal weight starting point
        initial_weights = np.array([1/len(self.tickers)] * len(self.tickers))
        
        if target == 'sharpe':
            result = sco.minimize(negative_sharpe, initial_weights, 
                                method='SLSQP', bounds=bounds, constraints=constraints)
        else:  # minimum variance
            result = sco.minimize(minimize_volatility, initial_weights,
                                method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = result.x
            opt_return, opt_volatility, opt_sharpe = portfolio_stats(optimal_weights)
            
            return {
                'weights': optimal_weights,
                'expected_return': opt_return,
                'volatility': opt_volatility,
                'sharpe_ratio': opt_sharpe
            }
        
        return None
    
    def generate_efficient_frontier(self, num_portfolios=100):
        """Generate efficient frontier for portfolio optimization"""
        if self.returns_df is None or len(self.returns_df.columns) < 2:
            return None
            
        returns = self.returns_df.mean() * 252
        cov_matrix = self.returns_df.cov() * 252
        
        # Generate target returns
        min_ret = returns.min()
        max_ret = returns.max()
        target_returns = np.linspace(min_ret, max_ret, num_portfolios)
        
        efficient_portfolios = []
        
        for target_return in target_returns:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(returns * x) - target_return}
            ]
            bounds = tuple((0, 1) for _ in range(len(self.tickers)))
            initial_weights = np.array([1/len(self.tickers)] * len(self.tickers))
            
            def portfolio_volatility(weights):
                return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            
            try:
                result = sco.minimize(portfolio_volatility, initial_weights,
                                    method='SLSQP', bounds=bounds, constraints=constraints)
                
                if result.success:
                    efficient_portfolios.append({
                        'return': target_return,
                        'volatility': result.fun,
                        'weights': result.x
                    })
            except:
                continue
        
        return efficient_portfolios


def create_advanced_portfolio_interface(tickers):
    """Create the advanced portfolio analysis interface"""
    
    st.markdown("""
    <div class="analytics-executive">
        <h3>Advanced Portfolio Analytics Laboratory</h3>
        <p>Modern Portfolio Theory & Institutional Risk Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize portfolio analyzer
    analyzer = AdvancedPortfolioAnalyzer(tickers)
    
    # Fetch data
    with st.spinner("Loading portfolio data and calculating analytics..."):
        portfolio_data = analyzer.fetch_portfolio_data()
        returns_matrix = analyzer.calculate_returns_matrix()
    
    if not portfolio_data:
        st.error("Unable to fetch portfolio data. Please check ticker symbols.")
        return
    
    # Portfolio Overview
    st.subheader("Portfolio Composition Overview")
    
    composition_data = []
    total_market_cap = sum([data.get('market_cap', 0) for data in portfolio_data.values()])
    
    for ticker, data in portfolio_data.items():
        weight = (data.get('market_cap', 0) / total_market_cap * 100) if total_market_cap > 0 else (100 / len(tickers))
        composition_data.append({
            'Ticker': ticker,
            'Company': data['name'][:30],
            'Sector': data['sector'],
            'Weight': f"{weight:.1f}%",
            'Price': f"${data['price']:.2f}",
            'Market Cap': f"${data.get('market_cap', 0)/1e9:.1f}B" if data.get('market_cap', 0) > 0 else "N/A",
            'P/E Ratio': f"{data.get('pe_ratio', 0):.1f}" if data.get('pe_ratio', 0) else "N/A",
            'Beta': f"{data.get('beta', 0):.2f}" if data.get('beta', 0) else "N/A"
        })
    
    composition_df = pd.DataFrame(composition_data)
    st.dataframe(composition_df, use_container_width=True, height=300)
    
    # Portfolio Performance Metrics
    portfolio_metrics = analyzer.calculate_portfolio_metrics()
    
    if portfolio_metrics:
        st.subheader("Portfolio Performance Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Expected Annual Return", f"{portfolio_metrics['annual_return']*100:.2f}%")
        
        with col2:
            st.metric("Annual Volatility", f"{portfolio_metrics['annual_volatility']*100:.2f}%")
        
        with col3:
            st.metric("Sharpe Ratio", f"{portfolio_metrics['sharpe_ratio']:.2f}")
        
        with col4:
            st.metric("Maximum Drawdown", f"{portfolio_metrics['max_drawdown']*100:.2f}%")
        
        # Risk Metrics
        st.subheader("Risk Assessment")
        
        risk_col1, risk_col2 = st.columns(2)
        
        with risk_col1:
            st.metric("Value at Risk (95%)", f"{portfolio_metrics['var_95']*100:.2f}%")
        
        with risk_col2:
            st.metric("Value at Risk (99%)", f"{portfolio_metrics['var_99']*100:.2f}%")
    
    # Correlation Analysis
    if analyzer.correlation_matrix is not None:
        st.subheader("Portfolio Correlation Analysis")
        
        fig_corr = px.imshow(
            analyzer.correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Asset Correlation Matrix"
        )
        
        fig_corr.update_layout(
            font=dict(family="Inter, sans-serif"),
            title_font=dict(size=18, color="#0f172a"),
            height=500
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
