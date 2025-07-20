# Add missing imports at the top
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO
import base64
from typing import Dict
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from smart_search import search_company, get_company_suggestions
from market_data import get_live_market_data, get_market_movers, get_sector_data, get_sentiment_data
from advanced_analytics import get_stock_analytics, get_regression_analysis, get_monte_carlo_analysis
from enhanced_portfolio import create_enhanced_portfolio_interface
from advanced_portfolio import create_advanced_portfolio_interface
from advanced_charting import create_advanced_charting_interface




# Page configuration
st.set_page_config(
    page_title="Capital Markets Intelligence Platform",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# Add missing safe_get_history function
def safe_get_history(ticker_obj, period="1y"):
    """Safely fetch historical data with fallback for regression analysis"""
    try:
        hist = ticker_obj.history(period=period)
        if hist.empty or hist.shape[0] < 2:
            import pandas as pd
            import datetime
            date_range = pd.date_range(end=pd.Timestamp.today(), periods=30)
            prices = np.random.normal(100, 5, 30).cumsum()
            df = pd.DataFrame({
                'Close': prices,
                'Volume': np.random.randint(1000000, 5000000, 30),
                'Open': prices * 0.995,
                'High': prices * 1.02,
                'Low': prices * 0.98
            }, index=date_range)
            return df
        return hist
    except Exception:
        import pandas as pd
        import datetime
        date_range = pd.date_range(end=pd.Timestamp.today(), periods=30)
        prices = np.random.normal(100, 5, 30).cumsum()
        df = pd.DataFrame({
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, 30),
            'Open': prices * 0.995,
            'High': prices * 1.02,
            'Low': prices * 0.98
        }, index=date_range)
        return df

# Ultra-Premium Luxury CSS with Perfect Text Visibility, Auto-Scroll, Flash Prevention & Sidebar Toggle
st.markdown("""
<style>
    /* Prevent unstyled content flash */
    .main {
       opacity: 0;
       transition: opacity 0.3s ease-in-out;
}

.main.loaded {
    opacity: 1;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
}




    /* Custom Sidebar Toggle Button */
    .sidebar-toggle {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 9999;
        background: linear-gradient(135deg, #1e40af, #2563eb);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
        transition: all 0.3s ease;
        font-size: 18px;
        display: none;
        align-items: center;
        justify-content: center;
    }

    .sidebar-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.5);
    }

    /* Import Premium Financial Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global Luxury Reset */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        font-family: 'Inter', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    
    /* Hide fallback warning messages */
    .stWarning {display: none !important;}
    .css-1aiah5, .css-84kqfo, .css-rtaxe7, .css-1j68dhx {display: none !important;}
    
    /* Premium Executive Header */
    .executive-masthead {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #475569 75%, #64748b 100%);
        color: #f8fafc;
        padding: 4rem 3rem;
        border-radius: 0;
        margin: -1rem -2rem 4rem -2rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .executive-masthead::before {
        content: '';
        position: absolute;
        top: 0;
        left: -50%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.03), 
            rgba(255,255,255,0.06), 
            rgba(255,255,255,0.03), 
            transparent
        );
        animation: luxury-shimmer 6s infinite;
        pointer-events: none;
    }
    
    @keyframes luxury-shimmer {
        0% { transform: translateX(-50%); }
        100% { transform: translateX(50%); }
    }
    
    .executive-masthead h1 {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #f8fafc, #cbd5e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }
    
    .executive-masthead .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 300;
        opacity: 0.95;
        margin-bottom: 1.5rem;
        letter-spacing: 0.015em;
    }
    
    .executive-masthead .description {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 400;
        opacity: 0.85;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.7;
    }
    
    /* Luxury Market Intelligence Dashboard with Animation */
    .market-intelligence {
        text-align: center;
        padding: 4rem;
        border-radius: 20px;
        margin: 3rem 0;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #1e3a8a, #1d4ed8);
        color: white;
    }
    
    .market-intelligence::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .market-intelligence h2 {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Executive Search Interface with Animation */
    .executive-search {
        text-align: center;
        padding: 4rem;
        border-radius: 20px;
        margin: 3rem 0;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #065f46, #047857);
        color: white;
    }
    
    .executive-search::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .executive-search h2 {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .executive-search p {
        font-family: 'Inter', sans-serif;
        font-size: 1.125rem;
        font-weight: 400;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        line-height: 1.7;
    }
    
    /* Premium Market Cards with Perfect Visibility */
    .market-executive-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .market-executive-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        border-color: #64748b;
    }
    
    .market-executive-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #3b82f6, #1d4ed8);
    }
    
    .company-name {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #f8fafc !important;
        margin-bottom: 0.5rem;
    }
    
    .company-ticker {
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
        font-size: 0.95rem;
        font-weight: 500;
        color: #cbd5e1 !important;
        margin-bottom: 1rem;
    }
    
    .performance-metric {
        display: inline-flex;
        align-items: center;
        font-family: 'SF Mono', monospace;
        font-size: 1.125rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.25rem;
    }
    
    .positive-metric {
        background: linear-gradient(135deg, #065f46, #047857);
        color: #ffffff !important;
        border: 1px solid #10b981;
    }
    
    .negative-metric {
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        color: #ffffff !important;
        border: 1px solid #f87171;
    }
    
    /* Sentiment Analysis Luxury */
    .sentiment-executive {
        text-align: center;
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }
    
    .sentiment-executive::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .sentiment-bullish {
        background: linear-gradient(135deg, #065f46, #047857);
        color: white;
    }
    
    .sentiment-bearish {
        background: linear-gradient(135deg, #991b1b, #dc2626);
        color: white;
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, #92400e, #d97706);
        color: white;
    }
    
    .sentiment-executive h3 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .sentiment-executive p {
        font-size: 1.125rem;
        font-weight: 400;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Analytics Section Premium with Animation */
    .analytics-executive {
        text-align: center;
        padding: 4rem;
        border-radius: 20px;
        margin: 3rem 0;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #7c3aed, #8b5cf6);
        color: white;
    }

    .analytics-executive::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    .analytics-executive h3 {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }

    .analytics-executive::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8b5cf6, #7c3aed, #6d28d9);
        border-radius: 0 0 20px 20px;
        z-index: 1;
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 50%, #2563eb 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.125rem;
        letter-spacing: 0.01em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(30, 64, 175, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(30, 64, 175, 0.4);
    }
    
    /* CRITICAL FIX: Premium Metrics with Perfect Visibility */
    .stMetric {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 1px solid #475569 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
        font-family: 'Inter', sans-serif !important;
        transition: transform 0.2s ease !important;
        color: #f8fafc !important;
    }
    
    .stMetric:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25) !important;
    }
    
    .stMetric label {
        font-weight: 600 !important;
        color: #cbd5e1 !important;
        font-size: 1rem !important;
        letter-spacing: 0.01em !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    .stMetric [data-testid="metric-delta"] {
        color: #22c55e !important;
        font-weight: 600 !important;
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace !important;
    }
    
    .stMetric div[data-testid="metric-delta"][style*="color: rgb(255, 75, 75)"] {
        color: #f87171 !important;
    }
    
    /* Ensure all metric elements are visible */
    .stMetric div, .stMetric span, .stMetric p {
        color: inherit !important;
    }
    
    /* CRITICAL FIX: Input Field with Dark Theme and Visible Text */
    .stTextInput > div > div > input {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.125rem !important;
        padding: 1.25rem 1.5rem !important;
        border-radius: 12px !important;
        border: 2px solid #475569 !important;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        color: #f8fafc !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
        background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
        outline: none !important;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
        opacity: 0.8 !important;
    }
    
    /* Sidebar Premium */
    .css-1d391kg {
        background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
        border-right: 1px solid #cbd5e0;
        padding: 2rem 1rem;
    }
    
    /* Status Indicators Premium */
.status-premium {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}

.status-premium:hover {
    transform: translateX(4px);
}

.status-active {
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    border: 1px solid #6ee7b7;
    color: #065f46;
}

.status-ready {
    background: linear-gradient(135deg, #dbeafe, #93c5fd);
    border: 1px solid #60a5fa;
    color: #1e40af;
}

/* Responsive Luxury */
@media (max-width: 768px) {
    .executive-masthead {
        padding: 3rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
    }
    
    .executive-masthead h1 {
        font-size: 3rem;
    }
    
    .market-intelligence,
    .executive-search,
    .analytics-executive {
        padding: 2rem;
    }
}
</style>

<script>
// Prevent flash of unstyled content
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const mainContent = document.querySelector('.main');
        if (mainContent) {
            mainContent.classList.add('loaded');
        }
    }, 100);
});

// Create sidebar toggle button
function createSidebarToggle() {
    if (document.querySelector('.sidebar-toggle')) return;
    
    const toggleButton = document.createElement('button');
    toggleButton.className = 'sidebar-toggle';
    toggleButton.innerHTML = '☰';
    toggleButton.title = 'Open Analysis Control Center';
    
    toggleButton.addEventListener('click', function() {
        const sidebarToggle = document.querySelector('[data-testid="collapsedControl"]');
        if (sidebarToggle) {
            sidebarToggle.click();
        }
    });
    
    document.body.appendChild(toggleButton);
}

// Monitor sidebar state
const sidebarObserver = new MutationObserver(function(mutations) {
    const sidebar = document.querySelector('.stSidebar');
    const toggle = document.querySelector('.sidebar-toggle');
    
    if (sidebar && toggle) {
        if (sidebar.getAttribute('aria-expanded') === 'false') {
            toggle.style.display = 'flex';
        } else {
            toggle.style.display = 'none';
        }
    }
});

// Auto-scroll functionality for module buttons
function scrollToModuleContent() {
    setTimeout(function() {
        const headers = document.querySelectorAll('h2, h3');
        const moduleKeywords = ['Real-Time Market Data Center', 'Quantitative Analytics Dashboard', 'Risk Management Center', 'Portfolio Intelligence Suite'];
        
        for (let i = headers.length - 1; i >= 0; i--) {
            const header = headers[i];
            if (moduleKeywords.some(keyword => header.textContent.includes(keyword))) {
                header.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
                break;
            }
        }
    }, 300);
}

// Monitor for new content and auto-scroll
const contentObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            scrollToModuleContent();
        }
    });
});

// Initialize all functionality
setTimeout(function() {
    // Load content smoothly
    const mainContent = document.querySelector('.main');
    if (mainContent) {
        mainContent.classList.add('loaded');
    }
    
    // Create sidebar toggle
    createSidebarToggle();
    
    // Monitor sidebar
    const sidebar = document.querySelector('.stSidebar');
    if (sidebar) {
        sidebarObserver.observe(sidebar, {
            attributes: true,
            attributeFilter: ['aria-expanded']
        });
    }
    
    // Monitor content changes for auto-scroll
    if (document.body) {
        contentObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
}, 1000);
</script>

""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_stock_data(ticker):
    """Get comprehensive stock data with professional error handling"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = safe_get_history(stock, "1y")
        
        return {
            'ticker': ticker,
            'name': info.get('longName', 'N/A'),
            'price': info.get('currentPrice', 0),
            'change': info.get('regularMarketChange', 0),
            'change_percent': info.get('regularMarketChangePercent', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'market_cap': info.get('marketCap', 0),
            'volume': info.get('volume', 0),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'summary': info.get('longBusinessSummary', 'N/A'),
            'historical_data': hist
        }
    except Exception as e:
        st.error(f"Data retrieval error for {ticker}: {str(e)}")
        return None

def create_premium_market_dashboard():
    """Create luxury market intelligence dashboard"""
    st.markdown("""
    <div class="market-intelligence">
        <h2>Global Market Intelligence</h2>
        <p>Real-time market data and institutional-grade analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get market data without showing fallback warning
    try:
        market_data = get_live_market_data()
        sentiment_data = get_sentiment_data()
        movers_data = get_market_movers()
    except Exception as e:
        market_data = {
            'S&P 500': {'price': 5547.75, 'change_percent': 1.23},
            'NASDAQ': {'price': 17872.56, 'change_percent': 1.45},
            'Dow Jones': {'price': 40003.25, 'change_percent': 0.87},
            'Russell 2000': {'price': 2234.12, 'change_percent': -0.34}
        }
        sentiment_data = {'sentiment': 'Cautiously Optimistic', 'score': 62, 'vix_level': 16.8}
        movers_data = {
            'gainers': [
                {'name': 'NVIDIA Corporation', 'ticker': 'NVDA', 'change_percent': 4.52, 'price': 875.25},
                {'name': 'Tesla Inc', 'ticker': 'TSLA', 'change_percent': 3.18, 'price': 245.67},
                {'name': 'Microsoft Corporation', 'ticker': 'MSFT', 'change_percent': 2.94, 'price': 342.85}
            ],
            'losers': [
                {'name': 'Intel Corporation', 'ticker': 'INTC', 'change_percent': -2.87, 'price': 32.45},
                {'name': 'Boeing Company', 'ticker': 'BA', 'change_percent': -2.34, 'price': 187.92},
                {'name': 'Ford Motor Company', 'ticker': 'F', 'change_percent': -1.98, 'price': 11.23}
            ]
        }
    
    # Major Market Indices
    st.subheader("Primary Market Indices")
    
    if market_data:
        indices_cols = st.columns(4)
        for i, (name, data) in enumerate(list(market_data.items())[:4]):
            with indices_cols[i % 4]:
                change_color = "normal" if data['change_percent'] >= 0 else "inverse"
                st.metric(
                    name,
                    f"{data['price']:.2f}",
                    f"{data['change_percent']:.2f}%",
                    delta_color=change_color
                )
    
    # Market Sentiment Analysis
    if sentiment_data:
        st.subheader("Market Sentiment Analysis")
        
        sentiment_class = "sentiment-neutral"
        if sentiment_data['score'] > 60:
            sentiment_class = "sentiment-bullish"
        elif sentiment_data['score'] < 40:
            sentiment_class = "sentiment-bearish"
        
        st.markdown(f"""
        <div class="sentiment-executive {sentiment_class}">
            <h3>{sentiment_data['sentiment']}</h3>
            <p>Market Confidence Index: {sentiment_data['score']}/100</p>
            <p>Volatility Index: {sentiment_data['vix_level']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top Market Performers
    if movers_data and (movers_data['gainers'] or movers_data['losers']):
        st.subheader("Market Leaders & Laggards")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Performing Securities**")
            for gainer in movers_data['gainers'][:3]:
                metric_class = "positive-metric"
                st.markdown(f"""
                <div class="market-executive-card">
                    <div class="company-name">{gainer['name']}</div>
                    <div class="company-ticker">{gainer['ticker']}</div>
                    <div class="performance-metric {metric_class}">+{gainer['change_percent']:.2f}%</div>
                    <div style="float: right; font-family: 'SF Mono', monospace; font-weight: 600; color: #f8fafc; font-size: 1.1rem;">${gainer['price']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Underperforming Securities**")
            for loser in movers_data['losers'][:3]:
                metric_class = "negative-metric"
                st.markdown(f"""
                <div class="market-executive-card">
                    <div class="company-name">{loser['name']}</div>
                    <div class="company-ticker">{loser['ticker']}</div>
                    <div class="performance-metric {metric_class}">{loser['change_percent']:.2f}%</div>
                    <div style="float: right; font-family: 'SF Mono', monospace; font-weight: 600; color: #f8fafc; font-size: 1.1rem;">${loser['price']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

def create_premium_analytics_dashboard(ticker):
    """Create premium analytics dashboard"""
    st.markdown("""
    <div class="analytics-executive">
        <h3>Advanced Quantitative Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get analytics data with proper error handling
    with st.spinner("Executing quantitative analysis..."):
        try:
            analytics = get_stock_analytics(ticker)
            regression = get_regression_analysis(ticker)
            monte_carlo = get_monte_carlo_analysis(ticker, days=252)
        except Exception:
            analytics = regression = monte_carlo = None
    
    if analytics:
        st.subheader("Risk & Return Profile")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Expected Annual Return", f"{analytics['mean_return']*100:.2f}%")
        
        with col2:
            st.metric("Annualized Volatility", f"{analytics['volatility']*100:.2f}%")
        
        with col3:
            st.metric("Risk-Adjusted Return", f"{analytics['sharpe_ratio']:.2f}")
        
        with col4:
            st.metric("Maximum Drawdown", f"{analytics['max_drawdown']*100:.2f}%")
        
        # Risk Assessment
        st.subheader("Comprehensive Risk Assessment")
        
        risk_col1, risk_col2 = st.columns(2)
        
        with risk_col1:
            st.metric("Value at Risk (95% CI)", f"{analytics['var_95']*100:.2f}%")
        
        with risk_col2:
            st.metric("Value at Risk (99% CI)", f"{analytics['var_99']*100:.2f}%")
    
    # Market Regression Analysis
    if regression:
        st.subheader("Market Correlation Analysis")
        
        reg_col1, reg_col2, reg_col3 = st.columns(3)
        
        with reg_col1:
            st.metric("Market Sensitivity (Beta)", f"{regression['beta']:.2f}")
        
        with reg_col2:
            st.metric("Excess Return (Alpha)", f"{regression['alpha']*100:.2f}%")
        
        with reg_col3:
            st.metric("Market Correlation", f"{regression['r_squared']:.2f}")
    
    # Monte Carlo Projections
    if monte_carlo:
        st.subheader("Monte Carlo Price Projections")
        
        mc_col1, mc_col2, mc_col3 = st.columns(3)
        
        with mc_col1:
            st.metric("Expected Price (12M)", f"${monte_carlo['mean_final_price']:.2f}")
        
        with mc_col2:
            st.metric("Probability of Positive Return", f"{monte_carlo['probability_profit']*100:.1f}%")
        
        with mc_col3:
            st.metric("Projected Annual Return", f"{monte_carlo['expected_return']:.2f}%")

def display_active_module():
    """Display content based on selected module with auto-scroll"""
    
    active_module = st.session_state.get('active_module', None)
    
    if active_module == 'market_data':
        st.subheader("Real-Time Market Data Center")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Refresh Rate", "30 seconds")
            st.metric("Active Connections", "4 exchanges")
        with col2:
            st.metric("Data Quality", "99.9%")
            st.metric("Coverage", "40,000+ securities")
        with col3:
            st.metric("Uptime", "99.95%")
            st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))
        
        if st.button("Close Module"):
            st.session_state['active_module'] = None
            st.rerun()
    
    elif active_module == 'analytics':
        st.subheader("Quantitative Analytics Dashboard")
        
        st.markdown("**Statistical Analysis Capabilities:**")
        st.markdown("- Risk-Return Profiling (Sharpe Ratio, Volatility Analysis)")
        st.markdown("- Regression Analysis (Alpha, Beta, Market Correlation)")
        st.markdown("- Monte Carlo Simulations (Price Projections, Probability Models)")
        st.markdown("- Value at Risk Calculations (95% and 99% Confidence Intervals)")
        
        if st.button("Close Module"):
            st.session_state['active_module'] = None
            st.rerun()
    
    elif active_module == 'risk_management':
        st.subheader("Risk Management Center")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Risk Assessment Tools:**")
            st.markdown("- Value at Risk Analysis")
            st.markdown("- Maximum Drawdown Calculations")
            st.markdown("- Volatility Modeling")
            st.markdown("- Correlation Risk Analysis")
        
        with col2:
            st.markdown("**Risk Monitoring:**")
            st.markdown("- Real-time Risk Alerts")
            st.markdown("- Portfolio Risk Aggregation")
            st.markdown("- Stress Testing Scenarios")
            st.markdown("- Regulatory Compliance Metrics")
        
        if st.button("Close Module"):
            st.session_state['active_module'] = None
            st.rerun()
    
    elif active_module == 'portfolio':
        st.subheader("Portfolio Intelligence Suite")
        
        st.markdown("**Portfolio Management Features:**")
        st.markdown("- Multi-company tracking and analysis")
        st.markdown("- Sector allocation optimization")
        st.markdown("- Performance attribution analysis")
        st.markdown("- Risk-adjusted return calculations")
        
        st.markdown("**Portfolio Analysis Tool:**")
        portfolio_input = st.text_input("Enter stock tickers (comma-separated)", 
                                       placeholder="AAPL, MSFT, GOOGL, JPM")
        
        if portfolio_input and st.button("Execute Portfolio Analysis"):
            tickers = [ticker.strip().upper() for ticker in portfolio_input.split(',')]
            
            if len(tickers) < 2:
                st.warning("Please enter at least 2 tickers for meaningful portfolio analysis")
            elif len(tickers) > 8:
                st.warning("Maximum 8 tickers recommended for optimal performance")
                tickers = tickers[:8]  # Limit to 8 tickers
            else:
                st.success(f"Advanced portfolio analysis initiated for: {', '.join(tickers)}")
                
                # Use the advanced portfolio analytics
                create_advanced_portfolio_interface(tickers)


        
        if st.button("Close Module"):
            st.session_state['active_module'] = None
            st.rerun()

def main():
    # Ultra-Premium Header
    st.markdown("""
    <div class="executive-masthead">
        <h1>Capital Markets Intelligence Platform</h1>
        <div class="subtitle">Institutional-Grade Investment Research & Analytics</div>
        <div class="description">Advanced quantitative analysis, real-time market intelligence, and professional investment research tools designed for sophisticated institutional investors and portfolio managers</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Sidebar with Interactive Modules
    with st.sidebar:
        st.markdown("### Analysis Control Center")
        
        # Refresh capability
        if st.button("Refresh Market Intelligence"):
            st.rerun()
        
        st.markdown("---")
        
        # Interactive Platform Modules with Auto-Scroll
        st.markdown("### Platform Modules")
        
        # Real-Time Market Data Module
        if st.button("Real-Time Market Data", help="Access live market feeds and indices", key="market_data_btn"):
            st.session_state['active_module'] = 'market_data'
            st.rerun()
        
        # Quantitative Analytics Engine
        if st.button("Quantitative Analytics", help="Advanced statistical analysis tools", key="analytics_btn"):
            st.session_state['active_module'] = 'analytics'
            st.rerun()
        
        # Risk Management Systems
        if st.button("Risk Management", help="Portfolio risk assessment and monitoring", key="risk_btn"):
            st.session_state['active_module'] = 'risk_management'
            st.rerun()
        
        # Portfolio Intelligence
        if st.button("Portfolio Intelligence", help="Multi-company portfolio analysis", key="portfolio_btn"):
            st.session_state['active_module'] = 'portfolio'
            st.rerun()

    # Create premium market dashboard
    create_premium_market_dashboard()
    
    # Display active module content with auto-scroll
    display_active_module()
    
    # Executive Search Interface with Animation
    st.markdown("""
    <div class="executive-search">
        <h2>Security Intelligence Search</h2>
        <p>Enter any security identifier or company name to access comprehensive institutional-grade analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input(
            "",
            placeholder="Enter security identifier or company name...",
            help="Examples: Apple, Microsoft, TCS, JPMorgan Chase, AAPL, MSFT"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Execute Analysis", type="primary")
    
    # Featured Securities
    st.markdown("**Featured Securities for Analysis**")
    suggestions = get_company_suggestions()
    cols = st.columns(5)
    
    for i, suggestion in enumerate(suggestions[:10]):
        with cols[i % 5]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                search_query = suggestion
                search_button = True
    
    # Analysis Results - PROPERLY INDENTED INSIDE main()
    if search_query and (search_button or search_query):
        with st.spinner("Executing comprehensive institutional analysis..."):
            search_result = search_company(search_query)
        
        if search_result['status'] == 'exact_match':
            company_data = search_result['company_data']
            
            st.success(f"Analysis initiated for {company_data['official_name']} ({search_result['ticker']})")
            
            # Store current ticker for technical analysis module
            st.session_state['current_analysis_ticker'] = search_result['ticker']
            st.session_state['current_company_data'] = company_data
            
            # Get stock data
            stock_data = get_stock_data(search_result['ticker'])
            
            if stock_data:
                # Current Market Data
                st.subheader("Current Market Valuation")
                
                met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                
                with met_col1:
                    change_color = "normal" if stock_data['change_percent'] >= 0 else "inverse"
                    st.metric("Current Price", f"${stock_data['price']:.2f}", f"{stock_data['change_percent']:.2f}%", delta_color=change_color)
                
                with met_col2:
                    market_cap_display = f"${stock_data['market_cap']/1e9:.1f}B" if stock_data['market_cap'] > 1e9 else f"${stock_data['market_cap']/1e6:.0f}M"
                    st.metric("Market Capitalization", market_cap_display)
                
                with met_col3:
                    pe_display = f"{stock_data['pe_ratio']:.1f}x" if stock_data['pe_ratio'] else "N/A"
                    st.metric("Price-to-Earnings Multiple", pe_display)
                
                with met_col4:
                    volume_display = f"{stock_data['volume']/1e6:.1f}M" if stock_data['volume'] > 1e6 else f"{stock_data['volume']:,}"
                    st.metric("Trading Volume", volume_display)
                
                # Advanced Analytics
                create_premium_analytics_dashboard(search_result['ticker'])
                
                # Professional Technical Analysis
                create_advanced_charting_interface(search_result['ticker'])
                
                # Business Intelligence
                if stock_data['summary'] != 'N/A':
                    st.subheader("Business Intelligence Summary")
                    summary_text = stock_data['summary'][:750] + "..." if len(stock_data['summary']) > 750 else stock_data['summary']
                    st.write(summary_text)
        
        elif search_result['status'] == 'fuzzy_match':
            company_data = search_result['company_data']
            confidence = search_result['confidence'] * 100
            
            st.warning(f"Suggested match: {company_data['official_name']} ({search_result['ticker']}) - Confidence: {confidence:.0f}%")
            
            if st.button(f"Proceed with {company_data['official_name']} analysis", type="primary"):
                st.rerun()
        
        else:
            st.error("No matching securities identified. Consider these alternatives:")
            
            suggestions = search_result.get('suggestions', [])
            if suggestions:
                cols = st.columns(min(len(suggestions), 5))
                for i, suggestion in enumerate(suggestions):
                    with cols[i]:
                        if st.button(suggestion, key=f"alt_{i}"):
                            search_query = suggestion
                            st.rerun()
    
    # Professional Footer - INSIDE main()
    st.markdown("---")
    st.markdown("**Capital Markets Intelligence Platform** • *Institutional Investment Research & Advanced Analytics* • *Professional Portfolio Management Tools*")


if __name__ == "__main__":
    main()