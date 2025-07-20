import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import yfinance as yf

class PortfolioComparison:
    """Advanced multi-company portfolio comparison and analysis"""
    
    def __init__(self, tickers):
        self.tickers = [ticker.strip().upper() for ticker in tickers]
        self.data = {}
        self.comparison_metrics = {}
    
    def fetch_portfolio_data(self):
        """Fetch data for all companies in portfolio"""
        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period="1y")
                
                self.data[ticker] = {
                    'name': info.get('longName', ticker),
                    'price': info.get('currentPrice', 0),
                    'change_percent': info.get('regularMarketChangePercent', 0),
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'sector': info.get('sector', 'N/A'),
                    'beta': info.get('beta', 0),
                    'dividend_yield': info.get('dividendYield', 0),
                    'profit_margin': info.get('profitMargins', 0),
                    'historical_data': hist
                }
            except Exception as e:
                st.warning(f"Could not fetch data for {ticker}: {str(e)}")
        
        return self.data
    
    def calculate_comparison_metrics(self):
        """Calculate comparative metrics across portfolio"""
        if not self.data:
            return None
        
        metrics = []
        for ticker, data in self.data.items():
            if data['historical_data'] is not None and not data['historical_data'].empty:
                returns = data['historical_data']['Close'].pct_change().dropna()
                
                metrics.append({
                    'Ticker': ticker,
                    'Company': data['name'][:30],
                    'Current Price': f"${data['price']:.2f}",
                    'Daily Change': f"{data['change_percent']:.2f}%",
                    'Market Cap': f"${data['market_cap']/1e9:.1f}B" if data['market_cap'] else "N/A",
                    'P/E Ratio': f"{data['pe_ratio']:.1f}" if data['pe_ratio'] else "N/A",
                    'Sector': data['sector'],
                    'Beta': f"{data['beta']:.2f}" if data['beta'] else "N/A",
                    'Volatility': f"{returns.std() * np.sqrt(252) * 100:.1f}%",
                    'YTD Return': f"{((data['price'] / data['historical_data']['Close'].iloc[0]) - 1) * 100:.1f}%"
                })
        
        return pd.DataFrame(metrics)
    
    def create_price_comparison_chart(self):
        """Create interactive price comparison chart"""
        fig = go.Figure()
        
        for ticker, data in self.data.items():
            if data['historical_data'] is not None and not data['historical_data'].empty:
                hist = data['historical_data']
                normalized_prices = (hist['Close'] / hist['Close'].iloc[0] * 100)
                
                fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=normalized_prices,
                    mode='lines',
                    name=f"{ticker} - {data['name'][:20]}",
                    line=dict(width=3),
                    hovertemplate=f'<b>{ticker}</b><br>' +
                                  'Date: %{x}<br>' +
                                  'Normalized Price: %{y:.1f}<br>' +
                                  '<extra></extra>'
                ))
        
        fig.update_layout(
            title="Portfolio Performance Comparison (Normalized to 100)",
            xaxis_title="Date",
            yaxis_title="Normalized Price (Base = 100)",
            hovermode='x unified',
            template="plotly_white",
            font=dict(family="Inter, sans-serif"),
            title_font=dict(size=20, color="#0f172a"),
            height=500,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig
    
    def create_sector_allocation_chart(self):
        """Create sector allocation pie chart"""
        sector_data = {}
        total_market_cap = 0
        
        for ticker, data in self.data.items():
            sector = data.get('sector', 'Unknown')
            market_cap = data.get('market_cap', 0)
            
            if market_cap > 0:
                total_market_cap += market_cap
                if sector in sector_data:
                    sector_data[sector] += market_cap
                else:
                    sector_data[sector] = market_cap
        
        if sector_data:
            sectors = list(sector_data.keys())
            values = [sector_data[sector] / total_market_cap * 100 for sector in sectors]
            
            fig = go.Figure(data=[go.Pie(
                labels=sectors,
                values=values,
                hole=0.4,
                textinfo='label+percent',
                textfont_size=12,
                marker=dict(
                    colors=px.colors.qualitative.Set3,
                    line=dict(color='#FFFFFF', width=2)
                )
            )])
            
            fig.update_layout(
                title="Portfolio Sector Allocation",
                font=dict(family="Inter, sans-serif"),
                title_font=dict(size=20, color="#0f172a"),
                height=400
            )
            
            return fig
        
        return None
    
    def calculate_portfolio_risk_metrics(self):
        """Calculate portfolio-level risk metrics"""
        if len(self.data) < 2:
            return None
        
        # Get returns for all stocks
        returns_data = {}
        for ticker, data in self.data.items():
            if data['historical_data'] is not None and not data['historical_data'].empty:
                returns = data['historical_data']['Close'].pct_change().dropna()
                returns_data[ticker] = returns
        
        if len(returns_data) < 2:
            return None
        
        # Create returns dataframe
        returns_df = pd.DataFrame(returns_data).dropna()
        
        # Calculate correlation matrix
        correlation_matrix = returns_df.corr()
        
        # Calculate portfolio metrics (assuming equal weights)
        weights = np.array([1/len(returns_df.columns)] * len(returns_df.columns))
        
        # Portfolio return
        portfolio_return = np.sum(returns_df.mean() * weights) * 252
        
        # Portfolio volatility
        portfolio_variance = np.dot(weights.T, np.dot(returns_df.cov() * 252, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Portfolio Sharpe ratio (assuming 2% risk-free rate)
        risk_free_rate = 0.02
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        
        return {
            'portfolio_return': portfolio_return,
            'portfolio_volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'correlation_matrix': correlation_matrix
        }

def create_portfolio_comparison_interface(tickers):
    """Create the portfolio comparison interface"""
    portfolio = PortfolioComparison(tickers)
    
    with st.spinner("Fetching portfolio data..."):
        data = portfolio.fetch_portfolio_data()
    
    if not data:
        st.error("Unable to fetch data for any of the provided tickers")
        return
    
    st.success(f"Successfully loaded data for {len(data)} securities")
    
    # Comparison Table
    st.subheader("Portfolio Comparison Table")
    comparison_df = portfolio.calculate_comparison_metrics()
    
    if comparison_df is not None:
        st.dataframe(
            comparison_df,
            use_container_width=True,
            height=400
        )
    
    # Price Performance Chart
    st.subheader("Relative Performance Analysis")
    price_chart = portfolio.create_price_comparison_chart()
    if price_chart:
        st.plotly_chart(price_chart, use_container_width=True)
    
    # Sector Allocation
    st.subheader("Sector Diversification")
    sector_chart = portfolio.create_sector_allocation_chart()
    if sector_chart:
        st.plotly_chart(sector_chart, use_container_width=True)
    else:
        st.info("Sector allocation unavailable - insufficient market cap data")
    
    # Portfolio Risk Metrics
    st.subheader("Portfolio Risk Analysis")
    risk_metrics = portfolio.calculate_portfolio_risk_metrics()
    
    if risk_metrics:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Portfolio Return (Annual)", f"{risk_metrics['portfolio_return']*100:.2f}%")
        
        with col2:
            st.metric("Portfolio Volatility", f"{risk_metrics['portfolio_volatility']*100:.2f}%")
        
        with col3:
            st.metric("Sharpe Ratio", f"{risk_metrics['sharpe_ratio']:.2f}")
        
        # Correlation Matrix
        st.subheader("Correlation Matrix")
        fig_corr = px.imshow(
            risk_metrics['correlation_matrix'],
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            title="Stock Correlation Matrix"
        )
        fig_corr.update_layout(
            font=dict(family="Inter, sans-serif"),
            title_font=dict(size=18, color="#0f172a"),
            height=400
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    else:
        st.info("Portfolio risk analysis requires at least 2 securities with historical data")

