import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class EnhancedPortfolioAnalyzer:
    """Advanced portfolio comparison and optimization engine"""
    
    def __init__(self, tickers):
        self.tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
        self.data = {}
        self.returns_df = None
        self.correlation_matrix = None
        
    def fetch_portfolio_data(self):
        """Fetch comprehensive data for all portfolio companies"""
        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period="2y")  # 2 years for better analysis
                
                if not hist.empty:
                    self.data[ticker] = {
                        'name': info.get('longName', ticker),
                        'price': info.get('currentPrice', hist['Close'].iloc[-1]),
                        'market_cap': info.get('marketCap', 0),
                        'pe_ratio': info.get('trailingPE', 0),
                        'beta': info.get('beta', 1.0),
                        'sector': info.get('sector', 'Unknown'),
                        'industry': info.get('industry', 'Unknown'),
                        'dividend_yield': info.get('dividendYield', 0),
                        'profit_margin': info.get('profitMargins', 0),
                        'revenue_growth': info.get('revenueGrowth', 0),
                        'historical_data': hist,
                        'returns': hist['Close'].pct_change().dropna()
                    }
            except Exception as e:
                st.warning(f"Could not fetch complete data for {ticker}: {str(e)}")
        
        return len(self.data) > 0
    
    def calculate_portfolio_metrics(self):
        """Calculate comprehensive portfolio comparison metrics"""
        if not self.data:
            return None
        
        # Calculate returns matrix
        returns_data = {}
        for ticker, data in self.data.items():
            if len(data['returns']) > 0:
                returns_data[ticker] = data['returns']
        
        self.returns_df = pd.DataFrame(returns_data).dropna()
        
        if self.returns_df.empty:
            return None
        
        # Calculate correlation matrix
        self.correlation_matrix = self.returns_df.corr()
        
        # Calculate metrics for each stock
        metrics = []
        for ticker in self.returns_df.columns:
            returns = self.returns_df[ticker]
            annual_return = returns.mean() * 252
            volatility = returns.std() * np.sqrt(252)
            sharpe = annual_return / volatility if volatility > 0 else 0
            
            metrics.append({
                'Ticker': ticker,
                'Company': self.data[ticker]['name'][:25] + '...' if len(self.data[ticker]['name']) > 25 else self.data[ticker]['name'],
                'Current Price': f"${self.data[ticker]['price']:.2f}",
                'Market Cap': self._format_market_cap(self.data[ticker]['market_cap']),
                'Annual Return': f"{annual_return*100:.1f}%",
                'Volatility': f"{volatility*100:.1f}%",
                'Sharpe Ratio': f"{sharpe:.2f}",
                'Beta': f"{self.data[ticker]['beta']:.2f}" if self.data[ticker]['beta'] else "N/A",
                'P/E Ratio': f"{self.data[ticker]['pe_ratio']:.1f}" if self.data[ticker]['pe_ratio'] else "N/A",
                'Sector': self.data[ticker]['sector']
            })
        
        return pd.DataFrame(metrics)
    
    def _format_market_cap(self, market_cap):
        """Format market cap for display"""
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.1f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.1f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.0f}M"
        else:
            return "N/A"
    
    def create_performance_comparison_chart(self):
        """Create normalized performance comparison chart"""
        if self.returns_df is None or self.returns_df.empty:
            return None
        
        # Calculate cumulative returns (normalized to 100)
        cumulative_returns = (1 + self.returns_df).cumprod() * 100
        
        fig = go.Figure()
        
        # Color palette for professional look
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
        
        for i, ticker in enumerate(cumulative_returns.columns):
            fig.add_trace(go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[ticker],
                mode='lines',
                name=f"{ticker} - {self.data[ticker]['name'][:20]}",
                line=dict(width=3, color=colors[i % len(colors)]),
                hovertemplate=f'<b>{ticker}</b><br>' +
                              'Date: %{x}<br>' +
                              'Normalized Value: %{y:.1f}<br>' +
                              '<extra></extra>'
            ))
        
        fig.update_layout(
            title="Portfolio Performance Comparison (Normalized to 100)",
            xaxis_title="Date",
            yaxis_title="Normalized Performance",
            hovermode='x unified',
            template="plotly_white",
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=18, color="#0f172a"),
            height=500,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_correlation_heatmap(self):
        """Create correlation heatmap visualization"""
        if self.correlation_matrix is None:
            return None
        
        fig = px.imshow(
            self.correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            title="Stock Correlation Matrix",
            labels=dict(color="Correlation")
        )
        
        fig.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=18, color="#0f172a"),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_risk_return_scatter(self):
        """Create risk-return scatter plot"""
        if self.returns_df is None or self.returns_df.empty:
            return None
        
        risk_return_data = []
        for ticker in self.returns_df.columns:
            returns = self.returns_df[ticker]
            annual_return = returns.mean() * 252
            volatility = returns.std() * np.sqrt(252)
            market_cap = self.data[ticker]['market_cap']
            
            risk_return_data.append({
                'Ticker': ticker,
                'Return': annual_return * 100,
                'Risk': volatility * 100,
                'Market_Cap': market_cap,
                'Company': self.data[ticker]['name']
            })
        
        df = pd.DataFrame(risk_return_data)
        
        fig = px.scatter(
            df,
            x='Risk',
            y='Return',
            size='Market_Cap',
            hover_name='Ticker',
            hover_data={'Company': True, 'Market_Cap': ':,.0f'},
            title="Risk-Return Analysis",
            labels={'Risk': 'Volatility (%)', 'Return': 'Annual Return (%)'}
        )
        
        fig.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=18, color="#0f172a"),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_sector_allocation_chart(self):
        """Create sector allocation pie chart"""
        if not self.data:
            return None
        
        sector_data = {}
        total_market_cap = 0
        
        for ticker, data in self.data.items():
            sector = data.get('sector', 'Unknown')
            market_cap = data.get('market_cap', 0)
            
            if market_cap > 0:
                total_market_cap += market_cap
                sector_data[sector] = sector_data.get(sector, 0) + market_cap
        
        if not sector_data or total_market_cap == 0:
            return None
        
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
            title="Portfolio Sector Allocation (by Market Cap)",
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=18, color="#0f172a"),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

def create_enhanced_portfolio_interface(tickers):
    """Create the enhanced portfolio comparison interface"""
    if len(tickers) < 2:
        st.warning("Please enter at least 2 tickers for portfolio comparison")
        return
    
    if len(tickers) > 8:
        st.warning("Maximum 8 tickers allowed for optimal performance")
        tickers = tickers[:8]
    
    # Initialize portfolio analyzer
    portfolio = EnhancedPortfolioAnalyzer(tickers)
    
    with st.spinner("Fetching comprehensive portfolio data..."):
        success = portfolio.fetch_portfolio_data()
    
    if not success:
        st.error("Unable to fetch data for any of the provided tickers")
        return
    
    st.success(f"Successfully analyzed {len(portfolio.data)} securities")
    
    # Calculate portfolio metrics
    metrics_df = portfolio.calculate_portfolio_metrics()
    
    if metrics_df is not None:
        # Portfolio Comparison Table
        st.subheader("Portfolio Comparison Matrix")
        st.dataframe(
            metrics_df,
            use_container_width=True,
            height=300
        )
        
        # Performance Comparison Chart
        st.subheader("Normalized Performance Analysis")
        performance_chart = portfolio.create_performance_comparison_chart()
        if performance_chart:
            st.plotly_chart(performance_chart, use_container_width=True)
        
        # Risk-Return Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk-Return Profile")
            risk_return_chart = portfolio.create_risk_return_scatter()
            if risk_return_chart:
                st.plotly_chart(risk_return_chart, use_container_width=True)
        
        with col2:
            st.subheader("Sector Diversification")
            sector_chart = portfolio.create_sector_allocation_chart()
            if sector_chart:
                st.plotly_chart(sector_chart, use_container_width=True)
            else:
                st.info("Sector allocation unavailable - insufficient market cap data")
        
        # Correlation Analysis
        st.subheader("Portfolio Correlation Analysis")
        correlation_chart = portfolio.create_correlation_heatmap()
        if correlation_chart:
            st.plotly_chart(correlation_chart, use_container_width=True)
            
            # Correlation insights
            if portfolio.correlation_matrix is not None:
                st.subheader("Diversification Insights")
                
                # Find highest and lowest correlations
                corr_values = portfolio.correlation_matrix.values
                np.fill_diagonal(corr_values, np.nan)  # Remove self-correlations
                
                max_corr = np.nanmax(corr_values)
                min_corr = np.nanmin(corr_values)
                avg_corr = np.nanmean(corr_values)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Highest Correlation", f"{max_corr:.2f}")
                
                with col2:
                    st.metric("Average Correlation", f"{avg_corr:.2f}")
                
                with col3:
                    st.metric("Lowest Correlation", f"{min_corr:.2f}")
                
                # Diversification recommendation
                if avg_corr > 0.7:
                    st.warning("High average correlation detected. Consider adding securities from different sectors for better diversification.")
                elif avg_corr < 0.3:
                    st.success("Excellent diversification - low average correlation indicates good risk distribution.")
                else:
                    st.info("Moderate diversification - correlation levels are within acceptable ranges.")
    
    else:
        st.error("Unable to calculate portfolio metrics. Please check ticker symbols and try again.")

