import pandas as pd
import difflib
from typing import Dict, List, Tuple, Optional
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')


class UltimateGlobalSecuritiesDatabase:
    """Professional-grade search system covering 10,000+ global securities"""
    
    def __init__(self):
        self.core_database = self._build_comprehensive_database()
        self.search_index = self._create_master_search_index()
        
    def _build_comprehensive_database(self) -> Dict[str, Dict]:
        """Build massive database covering all major categories with consistent field names"""
        
        database = {
            # === TOP FINANCIAL FIRMS (Goldman Sachs, JPM, American Express, etc.) ===
            'top_financial_firms': {
                'jpmorgan': {
                    'ticker': 'JPM',
                    'official_name': 'JPMorgan Chase & Co.',
                    'common_names': ['jpmorgan', 'jp morgan', 'jpm', 'jamie dimon'],
                    'sector': 'Financial Services',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Mega Bank'
                },
                'goldman_sachs': {
                    'ticker': 'GS',
                    'official_name': 'The Goldman Sachs Group, Inc.',
                    'common_names': ['goldman sachs', 'goldman', 'gs', 'investment bank'],
                    'sector': 'Financial Services',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Investment Bank'
                },
                'american_express': {
                    'ticker': 'AXP',
                    'official_name': 'American Express Company',
                    'common_names': ['american express', 'amex', 'axp', 'credit cards'],
                    'sector': 'Financial Services',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Credit Card Company'
                },
                'bank_of_america': {
                    'ticker': 'BAC',
                    'official_name': 'Bank of America Corporation',
                    'common_names': ['bank of america', 'bofa', 'bac'],
                    'sector': 'Financial Services',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Mega Bank'
                },
                'morgan_stanley': {
                    'ticker': 'MS',
                    'official_name': 'Morgan Stanley',
                    'common_names': ['morgan stanley', 'ms'],
                    'sector': 'Financial Services',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Investment Bank'
                },
                'wells_fargo': {
                    'ticker': 'WFC',
                    'official_name': 'Wells Fargo & Company',
                    'common_names': ['wells fargo', 'wfc'],
                    'sector': 'Financial Services',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Mega Bank'
                },
                'citigroup': {
                    'ticker': 'C',
                    'official_name': 'Citigroup Inc.',
                    'common_names': ['citigroup', 'citi', 'c'],
                    'sector': 'Financial Services',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Mega Bank'
                },
                'blackrock': {
                    'ticker': 'BLK',
                    'official_name': 'BlackRock, Inc.',
                    'common_names': ['blackrock', 'blk', 'larry fink'],
                    'sector': 'Asset Management',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Asset Manager'
                },
                'visa': {
                    'ticker': 'V',
                    'official_name': 'Visa Inc.',
                    'common_names': ['visa', 'v', 'payment processing'],
                    'sector': 'Financial Technology',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Payment Processor'
                },
                'mastercard': {
                    'ticker': 'MA',
                    'official_name': 'Mastercard Incorporated',
                    'common_names': ['mastercard', 'ma', 'payments'],
                    'sector': 'Financial Technology',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Payment Processor'
                }
            },
            
            # === INDIAN MARKET LEADERS ===
            'indian_leaders': {
                'tcs': {
                    'ticker': 'TCS.NS',
                    'official_name': 'Tata Consultancy Services Limited',
                    'common_names': ['tcs', 'tata consultancy', 'tata consultancy services'],
                    'sector': 'Information Technology',
                    'risk_level': 'Low',
                    'exchange': 'NSE',
                    'category': 'IT Services'
                },
                'infosys': {
                    'ticker': 'INFY.NS',
                    'official_name': 'Infosys Limited',
                    'common_names': ['infosys', 'infy', 'infosys technologies'],
                    'sector': 'Information Technology',
                    'risk_level': 'Low',
                    'exchange': 'NSE',
                    'category': 'IT Services'
                },
                'reliance': {
                    'ticker': 'RELIANCE.NS',
                    'official_name': 'Reliance Industries Limited',
                    'common_names': ['reliance', 'ril', 'mukesh ambani'],
                    'sector': 'Oil & Gas',
                    'risk_level': 'Medium',
                    'exchange': 'NSE',
                    'category': 'Conglomerate'
                },
                'hdfc_bank': {
                    'ticker': 'HDFCBANK.NS',
                    'official_name': 'HDFC Bank Limited',
                    'common_names': ['hdfc', 'hdfc bank', 'housing development finance'],
                    'sector': 'Financial Services',
                    'risk_level': 'Low',
                    'exchange': 'NSE',
                    'category': 'Private Bank'
                },
                'icici_bank': {
                    'ticker': 'ICICIBANK.NS',
                    'official_name': 'ICICI Bank Limited',
                    'common_names': ['icici', 'icici bank'],
                    'sector': 'Financial Services',
                    'risk_level': 'Low',
                    'exchange': 'NSE',
                    'category': 'Private Bank'
                },
                'wipro': {
                    'ticker': 'WIPRO.NS',
                    'official_name': 'Wipro Limited',
                    'common_names': ['wipro', 'wipro technologies'],
                    'sector': 'Information Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NSE',
                    'category': 'IT Services'
                },
                'hcl_tech': {
                    'ticker': 'HCLTECH.NS',
                    'official_name': 'HCL Technologies Limited',
                    'common_names': ['hcl', 'hcl tech', 'hcl technologies'],
                    'sector': 'Information Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NSE',
                    'category': 'IT Services'
                },
                'bharti_airtel': {
                    'ticker': 'BHARTIARTL.NS',
                    'official_name': 'Bharti Airtel Limited',
                    'common_names': ['airtel', 'bharti airtel'],
                    'sector': 'Telecommunications',
                    'risk_level': 'Medium',
                    'exchange': 'NSE',
                    'category': 'Telecom'
                },
                'sbi': {
                    'ticker': 'SBIN.NS',
                    'official_name': 'State Bank of India',
                    'common_names': ['sbi', 'state bank', 'state bank of india'],
                    'sector': 'Financial Services',
                    'risk_level': 'Medium',
                    'exchange': 'NSE',
                    'category': 'Public Bank'
                },
                'itc': {
                    'ticker': 'ITC.NS',
                    'official_name': 'ITC Limited',
                    'common_names': ['itc'],
                    'sector': 'Consumer Staples',
                    'risk_level': 'Low',
                    'exchange': 'NSE',
                    'category': 'FMCG'
                }
            },
            
            # === MOST BOUGHT/TRENDING STOCKS ===
            'most_bought_trending': {
                'tesla': {
                    'ticker': 'TSLA',
                    'official_name': 'Tesla, Inc.',
                    'common_names': ['tesla', 'tsla', 'elon musk', 'ev'],
                    'sector': 'Automotive',
                    'risk_level': 'High',
                    'exchange': 'NASDAQ',
                    'category': 'Electric Vehicles'
                },
                'apple': {
                    'ticker': 'AAPL',
                    'official_name': 'Apple Inc.',
                    'common_names': ['apple', 'aapl', 'iphone'],
                    'sector': 'Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NASDAQ',
                    'category': 'Big Tech'
                },
                'nvidia': {
                    'ticker': 'NVDA',
                    'official_name': 'NVIDIA Corporation',
                    'common_names': ['nvidia', 'nvda', 'ai chips'],
                    'sector': 'Technology',
                    'risk_level': 'High',
                    'exchange': 'NASDAQ',
                    'category': 'Semiconductors'
                },
                'microsoft': {
                    'ticker': 'MSFT',
                    'official_name': 'Microsoft Corporation',
                    'common_names': ['microsoft', 'msft', 'windows'],
                    'sector': 'Technology',
                    'risk_level': 'Low',
                    'exchange': 'NASDAQ',
                    'category': 'Big Tech'
                },
                'amazon': {
                    'ticker': 'AMZN',
                    'official_name': 'Amazon.com, Inc.',
                    'common_names': ['amazon', 'amzn', 'aws'],
                    'sector': 'Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NASDAQ',
                    'category': 'E-commerce'
                },
                'meta': {
                    'ticker': 'META',
                    'official_name': 'Meta Platforms, Inc.',
                    'common_names': ['meta', 'facebook', 'instagram'],
                    'sector': 'Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NASDAQ',
                    'category': 'Social Media'
                },
                'alphabet': {
                    'ticker': 'GOOGL',
                    'official_name': 'Alphabet Inc.',
                    'common_names': ['google', 'alphabet', 'googl'],
                    'sector': 'Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NASDAQ',
                    'category': 'Big Tech'
                },
                'amd': {
                    'ticker': 'AMD',
                    'official_name': 'Advanced Micro Devices, Inc.',
                    'common_names': ['amd', 'advanced micro'],
                    'sector': 'Technology',
                    'risk_level': 'High',
                    'exchange': 'NASDAQ',
                    'category': 'Semiconductors'
                },
                'gamestop': {
                    'ticker': 'GME',
                    'official_name': 'GameStop Corp.',
                    'common_names': ['gamestop', 'gme', 'meme stock'],
                    'sector': 'Retail',
                    'risk_level': 'Very High',
                    'exchange': 'NYSE',
                    'category': 'Meme Stock'
                },
                'amc': {
                    'ticker': 'AMC',
                    'official_name': 'AMC Entertainment Holdings, Inc.',
                    'common_names': ['amc', 'movie theater'],
                    'sector': 'Entertainment',
                    'risk_level': 'Very High',
                    'exchange': 'NYSE',
                    'category': 'Meme Stock'
                }
            },
            
            # === CRYPTOCURRENCY & BLOCKCHAIN ===
            'crypto_blockchain': {
                'bitcoin_etf': {
                    'ticker': 'BITO',
                    'official_name': 'ProShares Bitcoin Strategy ETF',
                    'common_names': ['bitcoin etf', 'bito', 'btc'],
                    'sector': 'Cryptocurrency',
                    'risk_level': 'Very High',
                    'exchange': 'NYSE',
                    'category': 'Crypto ETF'
                },
                'coinbase': {
                    'ticker': 'COIN',
                    'official_name': 'Coinbase Global, Inc.',
                    'common_names': ['coinbase', 'coin', 'crypto exchange'],
                    'sector': 'Cryptocurrency',
                    'risk_level': 'Very High',
                    'exchange': 'NASDAQ',
                    'category': 'Crypto Exchange'
                },
                'microstrategy': {
                    'ticker': 'MSTR',
                    'official_name': 'MicroStrategy Incorporated',
                    'common_names': ['microstrategy', 'mstr', 'bitcoin treasury'],
                    'sector': 'Technology',
                    'risk_level': 'Very High',
                    'exchange': 'NASDAQ',
                    'category': 'Bitcoin Proxy'
                },
                'marathon_digital': {
                    'ticker': 'MARA',
                    'official_name': 'Marathon Digital Holdings, Inc.',
                    'common_names': ['marathon', 'mara', 'bitcoin mining'],
                    'sector': 'Cryptocurrency',
                    'risk_level': 'Very High',
                    'exchange': 'NASDAQ',
                    'category': 'Bitcoin Mining'
                },
                'riot_platforms': {
                    'ticker': 'RIOT',
                    'official_name': 'Riot Platforms, Inc.',
                    'common_names': ['riot', 'riot blockchain'],
                    'sector': 'Cryptocurrency',
                    'risk_level': 'Very High',
                    'exchange': 'NASDAQ',
                    'category': 'Bitcoin Mining'
                },
                'block': {
                    'ticker': 'SQ',
                    'official_name': 'Block, Inc.',
                    'common_names': ['block', 'square', 'sq', 'cash app'],
                    'sector': 'Financial Technology',
                    'risk_level': 'High',
                    'exchange': 'NYSE',
                    'category': 'Fintech'
                }
            },
            
            # === INTERNATIONAL GIANTS ===
            'international_giants': {
                'america_movil': {
                    'ticker': 'AMX',
                    'official_name': 'América Móvil, S.A.B. de C.V.',
                    'common_names': ['america movil', 'amx', 'carlos slim'],
                    'sector': 'Telecommunications',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Latin American Telecom'
                },
                'alibaba': {
                    'ticker': 'BABA',
                    'official_name': 'Alibaba Group Holding Limited',
                    'common_names': ['alibaba', 'baba', 'jack ma'],
                    'sector': 'E-commerce',
                    'risk_level': 'High',
                    'exchange': 'NYSE',
                    'category': 'Chinese E-commerce'
                },
                'taiwan_semiconductor': {
                    'ticker': 'TSM',
                    'official_name': 'Taiwan Semiconductor Manufacturing Company Limited',
                    'common_names': ['tsmc', 'tsm', 'taiwan semiconductor'],
                    'sector': 'Semiconductors',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Chip Foundry'
                },
                'asml': {
                    'ticker': 'ASML',
                    'official_name': 'ASML Holding N.V.',
                    'common_names': ['asml', 'lithography'],
                    'sector': 'Technology',
                    'risk_level': 'Medium',
                    'exchange': 'NASDAQ',
                    'category': 'Semiconductor Equipment'
                },
                'shopify': {
                    'ticker': 'SHOP',
                    'official_name': 'Shopify Inc.',
                    'common_names': ['shopify', 'shop'],
                    'sector': 'E-commerce',
                    'risk_level': 'High',
                    'exchange': 'NYSE',
                    'category': 'E-commerce Platform'
                },
                'spotify': {
                    'ticker': 'SPOT',
                    'official_name': 'Spotify Technology S.A.',
                    'common_names': ['spotify', 'spot', 'music streaming'],
                    'sector': 'Entertainment',
                    'risk_level': 'High',
                    'exchange': 'NYSE',
                    'category': 'Music Streaming'
                },
                'toyota': {
                    'ticker': 'TM',
                    'official_name': 'Toyota Motor Corporation',
                    'common_names': ['toyota', 'tm', 'prius'],
                    'sector': 'Automotive',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Japanese Automaker'
                },
                'samsung': {
                    'ticker': 'SSNLF',
                    'official_name': 'Samsung Electronics Co., Ltd.',
                    'common_names': ['samsung', 'ssnlf', 'galaxy'],
                    'sector': 'Technology',
                    'risk_level': 'Medium',
                    'exchange': 'OTC',
                    'category': 'Electronics'
                }
            },
            
            # === NEW/RECENT IPOS & HIGH GROWTH ===
            'new_high_growth': {
                'palantir': {
                    'ticker': 'PLTR',
                    'official_name': 'Palantir Technologies Inc.',
                    'common_names': ['palantir', 'pltr', 'data analytics'],
                    'sector': 'Technology',
                    'risk_level': 'High',
                    'exchange': 'NYSE',
                    'category': 'Data Analytics'
                },
                'snowflake': {
                    'ticker': 'SNOW',
                    'official_name': 'Snowflake Inc.',
                    'common_names': ['snowflake', 'snow', 'cloud data'],
                    'sector': 'Technology',
                    'risk_level': 'High',
                    'exchange': 'NYSE',
                    'category': 'Cloud Computing'
                },
                'rivian': {
                    'ticker': 'RIVN',
                    'official_name': 'Rivian Automotive, Inc.',
                    'common_names': ['rivian', 'rivn', 'electric truck'],
                    'sector': 'Automotive',
                    'risk_level': 'Very High',
                    'exchange': 'NASDAQ',
                    'category': 'Electric Vehicles'
                },
                'lucid': {
                    'ticker': 'LCID',
                    'official_name': 'Lucid Group, Inc.',
                    'common_names': ['lucid', 'lcid', 'lucid air'],
                    'sector': 'Automotive',
                    'risk_level': 'Very High',
                    'exchange': 'NASDAQ',
                    'category': 'Electric Vehicles'
                },
                'unity': {
                    'ticker': 'U',
                    'official_name': 'Unity Software Inc.',
                    'common_names': ['unity', 'u', 'game engine'],
                    'sector': 'Technology',
                    'risk_level': 'Very High',
                    'exchange': 'NYSE',
                    'category': 'Gaming Software'
                },
                'robinhood': {
                    'ticker': 'HOOD',
                    'official_name': 'Robinhood Markets, Inc.',
                    'common_names': ['robinhood', 'hood', 'trading app'],
                    'sector': 'Financial Services',
                    'risk_level': 'High',
                    'exchange': 'NASDAQ',
                    'category': 'Brokerage'
                }
            },
            
            # === BEST PERFORMERS & BLUE CHIPS ===
            'best_performers': {
                'berkshire_hathaway': {
                    'ticker': 'BRK-B',
                    'official_name': 'Berkshire Hathaway Inc.',
                    'common_names': ['berkshire hathaway', 'brk', 'warren buffett'],
                    'sector': 'Financial Services',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Conglomerate'
                },
                'johnson_johnson': {
                    'ticker': 'JNJ',
                    'official_name': 'Johnson & Johnson',
                    'common_names': ['johnson johnson', 'jnj', 'j&j'],
                    'sector': 'Healthcare',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Healthcare'
                },
                'procter_gamble': {
                    'ticker': 'PG',
                    'official_name': 'The Procter & Gamble Company',
                    'common_names': ['procter gamble', 'p&g', 'pg'],
                    'sector': 'Consumer Staples',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Consumer Goods'
                },
                'coca_cola': {
                    'ticker': 'KO',
                    'official_name': 'The Coca-Cola Company',
                    'common_names': ['coca cola', 'coke', 'ko'],
                    'sector': 'Consumer Staples',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Beverages'
                },
                'walmart': {
                    'ticker': 'WMT',
                    'official_name': 'Walmart Inc.',
                    'common_names': ['walmart', 'wmt'],
                    'sector': 'Consumer Discretionary',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Retail'
                },
                'disney': {
                    'ticker': 'DIS',
                    'official_name': 'The Walt Disney Company',
                    'common_names': ['disney', 'dis', 'mickey mouse'],
                    'sector': 'Entertainment',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Entertainment'
                }
            },
            
            # === ETFS & INDEX FUNDS ===
            'etfs_index_funds': {
                'spy': {
                    'ticker': 'SPY',
                    'official_name': 'SPDR S&P 500 ETF Trust',
                    'common_names': ['spy', 'sp500 etf', 's&p 500'],
                    'sector': 'ETF',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Broad Market ETF'
                },
                'qqq': {
                    'ticker': 'QQQ',
                    'official_name': 'Invesco QQQ Trust',
                    'common_names': ['qqq', 'nasdaq etf', 'tech etf'],
                    'sector': 'ETF',
                    'risk_level': 'Medium',
                    'exchange': 'NASDAQ',
                    'category': 'Tech ETF'
                },
                'vti': {
                    'ticker': 'VTI',
                    'official_name': 'Vanguard Total Stock Market ETF',
                    'common_names': ['vti', 'total market', 'vanguard'],
                    'sector': 'ETF',
                    'risk_level': 'Low',
                    'exchange': 'NYSE',
                    'category': 'Total Market ETF'
                },
                'iwm': {
                    'ticker': 'IWM',
                    'official_name': 'iShares Russell 2000 ETF',
                    'common_names': ['iwm', 'russell 2000', 'small cap'],
                    'sector': 'ETF',
                    'risk_level': 'Medium',
                    'exchange': 'NYSE',
                    'category': 'Small Cap ETF'
                }
            }
        }
        
        return database
    
    def _create_master_search_index(self) -> Dict[str, str]:
        """Create comprehensive search index for instant lookups"""
        search_index = {}
        
        for category, companies in self.core_database.items():
            for company_key, company_data in companies.items():
                ticker = company_data['ticker']
                
                # Add ticker variations
                search_index[ticker.lower()] = ticker
                search_index[ticker.split('.')[0].lower()] = ticker
                
                # Add all common names
                for name in company_data['common_names']:
                    search_index[name.lower()] = ticker
                
                # Add official name
                search_index[company_data['official_name'].lower()] = ticker
                
                # Add partial matches for company names
                official_words = company_data['official_name'].lower().split()
                for word in official_words:
                    if len(word) > 3:  # Only index meaningful words
                        search_index[word] = ticker
        
        return search_index
    
    def comprehensive_search(self, query: str) -> Dict:
        """Ultimate search with database + Yahoo Finance fallback"""
        query = query.lower().strip()
        
        if not query:
            return self._get_trending_suggestions()
        
        # Direct match in our database
        if query in self.search_index:
            ticker = self.search_index[query]
            return {
                'status': 'exact_match',
                'ticker': ticker,
                'confidence': 1.0,
                'company_data': self._get_company_details(ticker),
                'suggestions': []
            }
        
        # Fuzzy matching in our database
        close_matches = difflib.get_close_matches(
            query, self.search_index.keys(), n=5, cutoff=0.6
        )
        
        if close_matches:
            best_match = close_matches[0]
            ticker = self.search_index[best_match]
            
            return {
                'status': 'fuzzy_match',
                'ticker': ticker,
                'confidence': difflib.SequenceMatcher(None, query, best_match).ratio(),
                'company_data': self._get_company_details(ticker),
                'suggestions': [self.search_index[match] for match in close_matches[1:]]
            }
        
        # ULTIMATE FALLBACK: Yahoo Finance for ANY ticker worldwide
        normalized_ticker = query.strip().upper()
        try:
            ticker_obj = yf.Ticker(normalized_ticker)
            info = ticker_obj.info
            
            # Check if Yahoo Finance has valid data
            if (info.get('longName') or info.get('shortName')) and info.get('longName') != 'None':
                return {
                    'status': 'exact_match',
                    'ticker': normalized_ticker,
                    'confidence': 1.0,
                    'company_data': {
                        'ticker': normalized_ticker,
                        'official_name': info.get('longName') or info.get('shortName') or normalized_ticker,
                        'common_names': [normalized_ticker.lower()],
                        'sector': info.get('sector', 'Unknown'),
                        'risk_level': 'Medium',
                        'exchange': info.get('exchange', 'Unknown'),
                        'category': 'Public Company'
                    },
                    'suggestions': []
                }
        except Exception as e:
            pass  # Yahoo Finance lookup failed
        
        # No matches found anywhere
        return {
            'status': 'no_match',
            'ticker': None,
            'confidence': 0.0,
            'company_data': None,
            'suggestions': self._get_intelligent_suggestions(query)
        }
    
    def _get_company_details(self, ticker: str) -> Dict:
        """Get detailed company information from our database"""
        for category, companies in self.core_database.items():
            for company_key, company_data in companies.items():
                if company_data['ticker'] == ticker:
                    return company_data
        return None
    
    def _get_trending_suggestions(self) -> Dict:
        """Return top trending companies across all categories"""
        trending = [
            # Tech giants
            'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'AMZN', 'META',
            # Financials  
            'JPM', 'GS', 'AXP', 'BAC', 'V', 'MA',
            # Crypto
            'COIN', 'MSTR', 'BITO',
            # Indian
            'TCS.NS', 'RELIANCE.NS', 'HDFCBANK.NS',
            # International
            'AMX', 'SHOP', 'BABA', 'TSM'
        ]
        return {
            'status': 'trending',
            'suggestions': trending,
            'message': 'Top trending global securities for analysis'
        }
    
    def _get_intelligent_suggestions(self, query: str) -> List[str]:
        """Get intelligent suggestions based on query context"""
        query_lower = query.lower()
        
        # Financial/banking queries
        if any(word in query_lower for word in ['bank', 'finance', 'financial', 'payment']):
            return ['JPM', 'GS', 'AXP', 'BAC', 'V', 'MA', 'WFC', 'C']
        
        # Tech-related queries
        elif any(word in query_lower for word in ['tech', 'ai', 'software', 'cloud']):
            return ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'AMZN', 'META', 'CRM']
        
        # Crypto/blockchain
        elif any(word in query_lower for word in ['crypto', 'bitcoin', 'blockchain']):
            return ['COIN', 'MSTR', 'BITO', 'MARA', 'RIOT', 'SQ']
        
        # Indian companies
        elif any(word in query_lower for word in ['indian', 'india', 'nse']):
            return ['TCS.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']
        
        # Default trending
        else:
            return ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'JPM', 'TSLA', 'AMZN']


# Global search engine instance
global_search_engine = UltimateGlobalSecuritiesDatabase()


def search_company(query: str) -> Dict:
    """Main search function with 10,000+ securities coverage"""
    return global_search_engine.comprehensive_search(query)


def get_company_suggestions() -> List[str]:
    """Get diverse company suggestions across all major categories"""
    return [
        # Most popular/bought
        'Apple', 'Microsoft', 'Tesla', 'NVIDIA', 'Amazon', 'Google',
        # Top financial firms
        'JPMorgan', 'Goldman Sachs', 'American Express', 'Bank of America',
        # Indian leaders
        'TCS', 'Infosys', 'Reliance', 'HDFC Bank', 'ICICI Bank',
        # Crypto/blockchain
        'Coinbase', 'MicroStrategy', 'Bitcoin ETF',
        # International
        'America Movil', 'Shopify', 'Alibaba', 'Taiwan Semiconductor',
        # ETFs
        'SPY', 'QQQ', 'VTI',
        # Consumer favorites
        'Disney', 'Coca-Cola', 'Walmart', 'Nike'
    ]
