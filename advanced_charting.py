import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class TechnicalAnalyzer:
    """Professional technical analysis and charting engine"""

    def __init__(self, ticker, period="1y"):
        self.ticker = ticker
        self.period = period
        self.data = None
        self.indicators = {}

    def fetch_stock_data(self):
        """Fetch comprehensive stock data for technical analysis"""
        try:
            stock = yf.Ticker(self.ticker)
            self.data = stock.history(period=self.period)

            if self.data.empty:
                return False

            # Calculate basic indicators immediately
            self.calculate_moving_averages()
            self.calculate_bollinger_bands()
            self.calculate_rsi()
            self.calculate_macd()
            self.calculate_volume_indicators()

            return True
        except Exception as e:
            st.error(f"Error fetching data for {self.ticker}: {str(e)}")
            return False

    def calculate_moving_averages(self):
        """Calculate Simple and Exponential Moving Averages"""
        if self.data is None:
            return

        # Simple Moving Averages
        self.indicators['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.indicators['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        self.indicators['SMA_200'] = self.data['Close'].rolling(window=200).mean()

        # Exponential Moving Averages
        self.indicators['EMA_12'] = self.data['Close'].ewm(span=12).mean()
        self.indicators['EMA_26'] = self.data['Close'].ewm(span=26).mean()
        self.indicators['EMA_50'] = self.data['Close'].ewm(span=50).mean()

    def calculate_bollinger_bands(self, window=20, num_std=2):
        """Calculate Bollinger Bands"""
        if self.data is None:
            return

        sma = self.data['Close'].rolling(window=window).mean()
        std = self.data['Close'].rolling(window=window).std()

        self.indicators['BB_Upper'] = sma + (std * num_std)
        self.indicators['BB_Lower'] = sma - (std * num_std)
        self.indicators['BB_Middle'] = sma

    def calculate_rsi(self, window=14):
        """Calculate Relative Strength Index"""
        if self.data is None:
            return

        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        self.indicators['RSI'] = 100 - (100 / (1 + rs))

    def calculate_macd(self, fast=12, slow=26, signal=9):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        if self.data is None:
            return

        ema_fast = self.data['Close'].ewm(span=fast).mean()
        ema_slow = self.data['Close'].ewm(span=slow).mean()

        self.indicators['MACD'] = ema_fast - ema_slow
        self.indicators['MACD_Signal'] = self.indicators['MACD'].ewm(span=signal).mean()
        self.indicators['MACD_Histogram'] = (
            self.indicators['MACD'] - self.indicators['MACD_Signal']
        )

    def calculate_volume_indicators(self):
        """Calculate volume-based indicators"""
        if self.data is None:
            return

        # Volume Moving Average
        self.indicators['Volume_MA'] = self.data['Volume'].rolling(window=20).mean()

        # On-Balance Volume
        obv = []
        obv_value = 0
        for i in range(len(self.data)):
            if i == 0:
                obv.append(self.data['Volume'].iloc[i])
            else:
                if self.data['Close'].iloc[i] > self.data['Close'].iloc[i - 1]:
                    obv_value += self.data['Volume'].iloc[i]
                elif self.data['Close'].iloc[i] < self.data['Close'].iloc[i - 1]:
                    obv_value -= self.data['Volume'].iloc[i]
                obv.append(obv_value)

        self.indicators['OBV'] = pd.Series(obv, index=self.data.index)

    def create_candlestick_chart(self):
        """Create professional candlestick chart with technical indicators"""
        if self.data is None:
            return None

        # Create subplots
        fig = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(
                f"{self.ticker} - Price & Volume Analysis",
                "RSI",
                "MACD",
                "Volume",
            ),
            row_width=[0.2, 0.1, 0.1, 0.1],
        )

        # Main candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name="Price",
                increasing_line_color="#00C851",
                decreasing_line_color="#FF4444",
            ),
            row=1,
            col=1,
        )

        # Moving Averages
        if 'SMA_20' in self.indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['SMA_20'],
                    line=dict(color="#FF6B35", width=2),
                    name="SMA 20",
                ),
                row=1,
                col=1,
            )

        if 'SMA_50' in self.indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['SMA_50'],
                    line=dict(color="#004E89", width=2),
                    name="SMA 50",
                ),
                row=1,
                col=1,
            )

        # Bollinger Bands
        if 'BB_Upper' in self.indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['BB_Upper'],
                    line=dict(color="rgba(128,128,128,0.3)", width=1),
                    name="BB Upper",
                ),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['BB_Lower'],
                    line=dict(color="rgba(128,128,128,0.3)", width=1),
                    name="BB Lower",
                    fill="tonexty",
                    fillcolor="rgba(128,128,128,0.1)",
                ),
                row=1,
                col=1,
            )

        # RSI
        if 'RSI' in self.indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['RSI'],
                    line=dict(color="#9C27B0", width=2),
                    name="RSI",
                ),
                row=2,
                col=1,
            )

            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        # MACD
        if 'MACD' in self.indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['MACD'],
                    line=dict(color="#2196F3", width=2),
                    name="MACD",
                ),
                row=3,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['MACD_Signal'],
                    line=dict(color="#FF9800", width=2),
                    name="Signal",
                ),
                row=3,
                col=1,
            )

            colors = [
                "green" if val >= 0 else "red"
                for val in self.indicators['MACD_Histogram']
            ]
            fig.add_trace(
                go.Bar(
                    x=self.data.index,
                    y=self.indicators['MACD_Histogram'],
                    name="MACD Histogram",
                    marker_color=colors,
                    opacity=0.7,
                ),
                row=3,
                col=1,
            )

        # Volume
        colors = [
            "green" if close >= open_ else "red"
            for close, open_ in zip(self.data['Close'], self.data['Open'])
        ]

        fig.add_trace(
            go.Bar(
                x=self.data.index,
                y=self.data['Volume'],
                name="Volume",
                marker_color=colors,
                opacity=0.7,
            ),
            row=4,
            col=1,
        )

        if 'Volume_MA' in self.indicators:
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.indicators['Volume_MA'],
                    line=dict(color="#FF6B35", width=2),
                    name="Volume MA",
                ),
                row=4,
                col=1,
            )

        # Layout
        fig.update_layout(
            title=f"{self.ticker} - Professional Technical Analysis",
            xaxis_rangeslider_visible=False,
            height=800,
            showlegend=True,
            template="plotly_white",
            font=dict(family="Inter, sans-serif", size=11),
            title_font=dict(size=20, color="#0f172a"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        fig.update_yaxes(title_text="Volume", row=4, col=1)

        return fig

    def get_technical_signals(self):
        """Generate trading signals based on technical indicators"""
        if self.data is None or not self.indicators:
            return {}

        signals = {}
        current_price = self.data['Close'].iloc[-1]

        # Moving Average Signals
        if 'SMA_20' in self.indicators and 'SMA_50' in self.indicators:
            sma_20 = self.indicators['SMA_20'].iloc[-1]
            sma_50 = self.indicators['SMA_50'].iloc[-1]

            if current_price > sma_20 > sma_50:
                signals['MA_Signal'] = 'BULLISH'
            elif current_price < sma_20 < sma_50:
                signals['MA_Signal'] = 'BEARISH'
            else:
                signals['MA_Signal'] = 'NEUTRAL'

        # RSI Signal
        if 'RSI' in self.indicators:
            rsi = self.indicators['RSI'].iloc[-1]
            if rsi > 70:
                signals['RSI_Signal'] = 'OVERBOUGHT'
            elif rsi < 30:
                signals['RSI_Signal'] = 'OVERSOLD'
            else:
                signals['RSI_Signal'] = 'NEUTRAL'

        # MACD Signal
        if 'MACD' in self.indicators and 'MACD_Signal' in self.indicators:
            macd = self.indicators['MACD'].iloc[-1]
            macd_signal = self.indicators['MACD_Signal'].iloc[-1]
            signals['MACD_Signal'] = 'BULLISH' if macd > macd_signal else 'BEARISH'

        # Bollinger Bands Signal
        if 'BB_Upper' in self.indicators and 'BB_Lower' in self.indicators:
            bb_upper = self.indicators['BB_Upper'].iloc[-1]
            bb_lower = self.indicators['BB_Lower'].iloc[-1]
            if current_price > bb_upper:
                signals['BB_Signal'] = 'OVERBOUGHT'
            elif current_price < bb_lower:
                signals['BB_Signal'] = 'OVERSOLD'
            else:
                signals['BB_Signal'] = 'NEUTRAL'

        return signals

    def get_support_resistance_levels(self):
        """Calculate support and resistance levels"""
        if self.data is None:
            return {}

        recent_data = self.data.tail(50)
        resistance = recent_data['High'].quantile(0.95)
        support = recent_data['Low'].quantile(0.05)

        return {
            'resistance': resistance,
            'support': support,
            'current_price': self.data['Close'].iloc[-1],
        }


def create_advanced_charting_interface(ticker):
    """Create the advanced charting interface"""
    
    st.markdown("""
    <div class="analytics-executive">
        <h3>Professional Technical Analysis Suite</h3>
        <p>Bloomberg Terminal-Grade Charts & Indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Time period selector with unique keys
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### Technical Analysis for {ticker}")
        st.markdown("*Professional-grade technical indicators and market signals*")
    
    with col2:
        period = st.selectbox(
            "Time Period",
            options=["1mo", "3mo", "6mo", "1y", "2y"],
            index=3,
            key=f"period_{ticker}_{id(ticker)}",
            help="Select time period for analysis"
        )
    
    with col3:
        chart_style = st.selectbox(
            "Chart Style",
            options=["Candlestick", "Line", "OHLC"],
            index=0,
            key=f"style_{ticker}_{id(ticker)}"
        )
    
    st.markdown("")
    
    # Initialize technical analyzer
    analyzer = TechnicalAnalyzer(ticker, period)
    
    # Fetch data and create charts
    with st.spinner("Loading technical analysis..."):
        success = analyzer.fetch_stock_data()
    
    if not success:
        st.error(f"Unable to fetch technical data for {ticker}")
        return
    
    st.markdown("---")
    
    # Main technical chart
    st.markdown("### Price Action & Technical Indicators")
    st.markdown("*Interactive candlestick chart with professional technical indicators*")
    
    chart = analyzer.create_candlestick_chart()
    if chart:
        st.plotly_chart(chart, use_container_width=True)
    
    st.markdown("---")
    
    # Technical signals and analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Trading Signals")
        st.markdown("*Real-time market signals based on technical indicators*")
        
        signals = analyzer.get_technical_signals()
        if signals:
            for signal_name, signal_value in signals.items():
                pretty_name = signal_name.replace('_', ' ')
                if signal_value == 'BULLISH':
                    st.success(f"{pretty_name}: {signal_value}")
                elif signal_value == 'BEARISH':
                    st.error(f"{pretty_name}: {signal_value}")
                elif signal_value in ['OVERBOUGHT', 'OVERSOLD']:
                    st.warning(f"{pretty_name}: {signal_value}")
                else:
                    st.info(f"{pretty_name}: {signal_value}")
        else:
            st.info("No clear signals at current levels")
    
    with col2:
        st.markdown("### Support & Resistance")
        st.markdown("*Key price levels and risk analysis*")
        
        levels = analyzer.get_support_resistance_levels()
        
        if levels:
            current_price = levels['current_price']
            resistance = levels['resistance']
            support = levels['support']
            
            st.metric("Current Price", f"${current_price:.2f}")
            st.metric("Resistance Level", f"${resistance:.2f}", 
                     f"{((resistance - current_price) / current_price * 100):+.1f}%")
            st.metric("Support Level", f"${support:.2f}", 
                     f"{((support - current_price) / current_price * 100):+.1f}%")
            
            # Risk/Reward Analysis
            if current_price < resistance and current_price > support:
                upside = (resistance - current_price) / current_price * 100
                downside = (current_price - support) / current_price * 100
                risk_reward = upside / downside if downside > 0 else 0
                
                st.markdown("#### Risk/Reward Analysis")
                col_risk, col_reward, col_ratio = st.columns(3)
                
                with col_risk:
                    st.metric("Downside Risk", f"{downside:.1f}%")
                
                with col_reward:
                    st.metric("Upside Potential", f"{upside:.1f}%")
                
                with col_ratio:
                    st.metric("Risk/Reward Ratio", f"{risk_reward:.2f}")
                
                if risk_reward > 2:
                    st.success("Favorable risk/reward profile")
                elif risk_reward > 1:
                    st.info("Acceptable risk/reward profile")
                else:
                    st.warning("Unfavorable risk/reward profile")
    
    # Technical indicators summary
    st.markdown("---")
    st.markdown("### Technical Indicators Summary")
    
    if analyzer.indicators:
        summary_data = []
        
        if 'RSI' in analyzer.indicators:
            rsi_current = analyzer.indicators['RSI'].iloc[-1]
            summary_data.append({
                'Indicator': 'RSI (14)',
                'Current Value': f"{rsi_current:.2f}",
                'Signal': 'Overbought' if rsi_current > 70 else 'Oversold' if rsi_current < 30 else 'Neutral',
                'Description': 'Momentum oscillator measuring speed and magnitude of price changes'
            })
        
        if 'MACD' in analyzer.indicators:
            macd_current = analyzer.indicators['MACD'].iloc[-1]
            macd_signal = analyzer.indicators['MACD_Signal'].iloc[-1]
            summary_data.append({
                'Indicator': 'MACD',
                'Current Value': f"{macd_current:.4f}",
                'Signal': 'Bullish' if macd_current > macd_signal else 'Bearish',
                'Description': 'Trend-following momentum indicator'
            })
        
        if 'SMA_20' in analyzer.indicators:
            sma_20 = analyzer.indicators['SMA_20'].iloc[-1]
            current_price = analyzer.data['Close'].iloc[-1]
            summary_data.append({
                'Indicator': 'SMA 20',
                'Current Value': f"${sma_20:.2f}",
                'Signal': 'Above' if current_price > sma_20 else 'Below',
                'Description': '20-day Simple Moving Average - short-term trend'
            })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, height=200)
    
    # Professional insights
    st.markdown("---")
    st.markdown("### Technical Analysis Insights")
    
    with st.expander("Understanding Technical Indicators", expanded=False):
        st.markdown("""
        **Key Technical Indicators Explained:**
        
        - **RSI (Relative Strength Index)**: Measures momentum. Values above 70 suggest overbought conditions, below 30 suggest oversold.
        
        - **MACD (Moving Average Convergence Divergence)**: Shows relationship between two moving averages. Signal line crossovers indicate potential buy/sell opportunities.
        
        - **Bollinger Bands**: Price channels based on standard deviation. Prices touching upper band may indicate overbought conditions.
        
        - **Moving Averages**: Smooth out price data to identify trend direction. Price above MA generally indicates uptrend.
        
        - **Volume Analysis**: Confirms price movements. High volume on price increases suggests strong bullish sentiment.
        """)
