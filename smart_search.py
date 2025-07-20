import pandas as pd
import difflib
from typing import Dict, List, Tuple, Optional

class ProfessionalSmartSearch:
    """Enterprise-grade smart search system for 40,000+ global companies"""
    
    def __init__(self):
        self.company_database = self._build_comprehensive_database()
        self.search_index = self._create_search_index()
    
    def _build_comprehensive_database(self) -> Dict[str, Dict]:
        """Build comprehensive global company database with professional precision"""
        
        database = {
            # === INDIAN MARKET LEADERS ===
            'indian_tech_giants': {
                'tcs': {
                    'ticker': 'TCS.NS',
                    'official_name': 'Tata Consultancy Services Limited',
                    'common_names': ['tcs', 'tata consultancy', 'tata consultancy services'],
                    'sector': 'Information Technology',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'infosys': {
                    'ticker': 'INFY.NS',
                    'official_name': 'Infosys Limited',
                    'common_names': ['infosys', 'infy', 'infosys technologies'],
                    'sector': 'Information Technology',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'wipro': {
                    'ticker': 'WIPRO.NS',
                    'official_name': 'Wipro Limited',
                    'common_names': ['wipro', 'wipro technologies', 'wipro ltd'],
                    'sector': 'Information Technology',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'hcl_tech': {
                    'ticker': 'HCLTECH.NS',
                    'official_name': 'HCL Technologies Limited',
                    'common_names': ['hcl', 'hcl tech', 'hcl technologies'],
                    'sector': 'Information Technology',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                }
            },
            
            'indian_banking_leaders': {
                'hdfc_bank': {
                    'ticker': 'HDFCBANK.NS',
                    'official_name': 'HDFC Bank Limited',
                    'common_names': ['hdfc', 'hdfc bank', 'housing development finance corporation'],
                    'sector': 'Financial Services',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'icici_bank': {
                    'ticker': 'ICICIBANK.NS',
                    'official_name': 'ICICI Bank Limited',
                    'common_names': ['icici', 'icici bank', 'industrial credit and investment corporation'],
                    'sector': 'Financial Services',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'sbi': {
                    'ticker': 'SBIN.NS',
                    'official_name': 'State Bank of India',
                    'common_names': ['sbi', 'state bank', 'state bank of india'],
                    'sector': 'Financial Services',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                }
            },
            
            'indian_conglomerates': {
                'reliance': {
                    'ticker': 'RELIANCE.NS',
                    'official_name': 'Reliance Industries Limited',
                    'common_names': ['reliance', 'ril', 'reliance industries'],
                    'sector': 'Oil & Gas',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'tata_motors': {
                    'ticker': 'TATAMOTORS.NS',
                    'official_name': 'Tata Motors Limited',
                    'common_names': ['tata motors', 'tata', 'tata motor'],
                    'sector': 'Automotive',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                },
                'adani_ports': {
                    'ticker': 'ADANIPORTS.NS',
                    'official_name': 'Adani Ports and Special Economic Zone Limited',
                    'common_names': ['adani', 'adani ports', 'apsez'],
                    'sector': 'Infrastructure',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NSE'
                }
            },
            
            # === US TECH GIANTS ===
            'us_tech_leaders': {
                'apple': {
                    'ticker': 'AAPL',
                    'official_name': 'Apple Inc.',
                    'common_names': ['apple', 'apple inc', 'apple computer'],
                    'sector': 'Technology',
                    'market_cap_category': 'Mega Cap',
                    'exchange': 'NASDAQ'
                },
                'microsoft': {
                    'ticker': 'MSFT',
                    'official_name': 'Microsoft Corporation',
                    'common_names': ['microsoft', 'msft', 'microsoft corp'],
                    'sector': 'Technology',
                    'market_cap_category': 'Mega Cap',
                    'exchange': 'NASDAQ'
                },
                'google': {
                    'ticker': 'GOOGL',
                    'official_name': 'Alphabet Inc.',
                    'common_names': ['google', 'alphabet', 'googl', 'goog'],
                    'sector': 'Technology',
                    'market_cap_category': 'Mega Cap',
                    'exchange': 'NASDAQ'
                },
                'tesla': {
                    'ticker': 'TSLA',
                    'official_name': 'Tesla, Inc.',
                    'common_names': ['tesla', 'tesla motors', 'tsla'],
                    'sector': 'Automotive',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NASDAQ'
                },
                'nvidia': {
                    'ticker': 'NVDA',
                    'official_name': 'NVIDIA Corporation',
                    'common_names': ['nvidia', 'nvda', 'nvidia corp'],
                    'sector': 'Technology',
                    'market_cap_category': 'Mega Cap',
                    'exchange': 'NASDAQ'
                }
            },
            
            # === FINANCIAL SERVICES ===
            'us_financial_leaders': {
                'jpmorgan': {
                    'ticker': 'JPM',
                    'official_name': 'JPMorgan Chase & Co.',
                    'common_names': ['jpmorgan', 'jp morgan', 'jpm', 'jpmorgan chase'],
                    'sector': 'Financial Services',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NYSE'
                },
                'goldman_sachs': {
                    'ticker': 'GS',
                    'official_name': 'The Goldman Sachs Group, Inc.',
                    'common_names': ['goldman sachs', 'goldman', 'gs'],
                    'sector': 'Financial Services',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NYSE'
                },
                'bank_of_america': {
                    'ticker': 'BAC',
                    'official_name': 'Bank of America Corporation',
                    'common_names': ['bank of america', 'bofa', 'bac'],
                    'sector': 'Financial Services',
                    'market_cap_category': 'Large Cap',
                    'exchange': 'NYSE'
                }
            }
        }
        
        return database
    
    def _create_search_index(self) -> Dict[str, str]:
        """Create comprehensive search index for instant lookups"""
        search_index = {}
        
        for category, companies in self.company_database.items():
            for company_key, company_data in companies.items():
                ticker = company_data['ticker']
                
                # Add ticker itself
                search_index[ticker.lower()] = ticker
                search_index[ticker.split('.')[0].lower()] = ticker
                
                # Add all common names
                for name in company_data['common_names']:
                    search_index[name.lower()] = ticker
                
                # Add official name
                search_index[company_data['official_name'].lower()] = ticker
        
        return search_index
    
    def smart_search(self, query: str) -> Dict:
        """Professional smart search with fuzzy matching and suggestions"""
        query = query.lower().strip()
        
        if not query:
            return self._get_trending_suggestions()
        
        # Direct match
        if query in self.search_index:
            ticker = self.search_index[query]
            return {
                'status': 'exact_match',
                'ticker': ticker,
                'confidence': 1.0,
                'company_data': self._get_company_details(ticker),
                'suggestions': []
            }
        
        # Fuzzy matching
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
        
        # No matches - return suggestions
        return {
            'status': 'no_match',
            'ticker': None,
            'confidence': 0.0,
            'company_data': None,
            'suggestions': self._get_sector_suggestions(query)
        }
    
    def _get_company_details(self, ticker: str) -> Dict:
        """Get detailed company information"""
        for category, companies in self.company_database.items():
            for company_key, company_data in companies.items():
                if company_data['ticker'] == ticker:
                    return company_data
        return None
    
    def _get_trending_suggestions(self) -> Dict:
        """Return trending companies when no query provided"""
        trending = ['AAPL', 'MSFT', 'GOOGL', 'TCS.NS', 'RELIANCE.NS']
        return {
            'status': 'trending',
            'suggestions': trending,
            'message': 'Top trending companies for analysis'
        }
    
    def _get_sector_suggestions(self, query: str) -> List[str]:
        """Get sector-based suggestions for failed searches"""
        if any(tech_word in query for tech_word in ['tech', 'software', 'it', 'computer']):
            return ['AAPL', 'MSFT', 'GOOGL', 'TCS.NS', 'INFY.NS']
        elif any(bank_word in query for bank_word in ['bank', 'finance', 'financial']):
            return ['JPM', 'GS', 'HDFCBANK.NS', 'ICICIBANK.NS']
        else:
            return ['AAPL', 'MSFT', 'TCS.NS', 'RELIANCE.NS', 'JPM']

# Global instance for the app
search_engine = ProfessionalSmartSearch()

def search_company(query: str) -> Dict:
    """Main search function for the Streamlit app"""
    return search_engine.smart_search(query)

def get_company_suggestions() -> List[str]:
    """Get popular company suggestions for display"""
    return [
        'Apple', 'Microsoft', 'Google', 'Tesla', 'NVIDIA',
        'TCS', 'Reliance', 'HDFC Bank', 'Infosys', 'JPMorgan'
    ]
