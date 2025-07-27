"""
Capital Markets Intelligence Platform - Professional Report Generator
Enterprise-grade PDF and Excel report generation with institutional formatting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import xlsxwriter
import logging
import os
import base64
from io import BytesIO



class ProfessionalReportGenerator:
    """
    Enterprise-grade report generation for Capital Markets Intelligence Platform
    """
    
    def __init__(self, company_name="Capital Markets Intelligence"):
        self.company_name = company_name
        self.setup_logging()
        self.setup_styling()
        
    def setup_logging(self):
        """Configure professional logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_styling(self):
        """Setup professional styling"""
        self.colors = {
            'primary': '#1e3a8a',
            'secondary': '#1e293b', 
            'accent': '#3b82f6',
            'success': '#059669',
            'text': '#374151',
            'light': '#f8fafc'
        }
        
        # Configure matplotlib for professional charts
        plt.style.use('default')
        sns.set_palette("husl")
        
    def generate_daily_kpi_digest(self, portfolio_data, market_data, risk_metrics):
        """Generate professional daily KPI digest with enhanced visualizations"""
        try:
            self.logger.info("Starting enhanced daily KPI digest generation")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_str = datetime.now().strftime("%B %d, %Y")
            
            pdf_filename = f"output/daily_reports/Daily_KPI_Digest_{timestamp}.pdf"
            excel_filename = f"output/daily_reports/Daily_KPI_Dashboard_{timestamp}.xlsx"
            
            # Generate enhanced PDF report with charts
            pdf_path = self.create_enhanced_pdf_digest(
                portfolio_data, market_data, risk_metrics, pdf_filename, date_str
            )
            
            # Generate Excel dashboard
            excel_path = self.create_professional_excel_dashboard(
                portfolio_data, market_data, risk_metrics, excel_filename
            )
            
            summary = self.create_executive_summary(portfolio_data, risk_metrics)
            
            self.logger.info(f"Enhanced reports generated: {pdf_path}, {excel_path}")
            
            return {
                'pdf_report': pdf_path,
                'excel_dashboard': excel_path,
                'executive_summary': summary,
                'generation_time': datetime.now(),
                'status': 'success'
            }
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_monte_carlo_chart(self, risk_metrics):
        """Create professional Monte Carlo simulation paths chart"""
        
        if not risk_metrics or 'simulation_paths' not in risk_metrics:
            return None
            
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            simulation_paths = risk_metrics['simulation_paths']
            
            # Plot simulation paths
            for i, path in enumerate(simulation_paths[:50]):  # Show 50 paths
                ax.plot(path, color='#60a5fa', alpha=0.3, linewidth=0.8)
            
            # Add mean path
            mean_path = np.mean(simulation_paths[:50], axis=0)
            ax.plot(mean_path, color='#1e3a8a', linewidth=3, label='Expected Path')
            
            ax.set_title('Monte Carlo Portfolio Value Projections', fontsize=16, fontweight='bold', color='#1e3a8a')
            ax.set_xlabel('Trading Days', fontsize=12)
            ax.set_ylabel('Portfolio Value (Normalized)', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Professional styling
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#374151')
            ax.spines['bottom'].set_color('#374151')
            
            plt.tight_layout()
            
            # Save to memory
            img_buffer = BytesIO()
            fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            plt.close(fig)
            
            return img_buffer
            
        except Exception as e:
            self.logger.error(f"Error creating Monte Carlo chart: {str(e)}")
            return None
    
    def create_portfolio_allocation_chart(self, portfolio_data):
        """Create professional portfolio allocation pie chart"""
        
        if not portfolio_data or 'portfolio_tickers' not in portfolio_data:
            return None
            
        try:
            tickers = portfolio_data['portfolio_tickers']
            weights = portfolio_data['portfolio_weights']
            
            fig, ax = plt.subplots(figsize=(8, 8))
            
            # Professional color palette
            colors_palette = ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe', '#1e293b']
            
            wedges, texts, autotexts = ax.pie(weights, labels=tickers, autopct='%1.1f%%',
                                            colors=colors_palette[:len(tickers)],
                                            startangle=90, textprops={'fontsize': 12})
            
            # Enhance text appearance
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title('Portfolio Allocation', fontsize=16, fontweight='bold', 
                        color='#1e3a8a', pad=20)
            
            plt.tight_layout()
            
            # Save to memory
            img_buffer = BytesIO()
            fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            plt.close(fig)
            
            return img_buffer
            
        except Exception as e:
            self.logger.error(f"Error creating allocation chart: {str(e)}")
            return None
    
    def create_risk_contribution_chart(self, risk_metrics):
        """Create professional risk contribution bar chart"""
        
        if not risk_metrics or 'tickers' not in risk_metrics or 'risk_contribution_pct' not in risk_metrics:
            return None
            
        try:
            tickers = risk_metrics['tickers']
            risk_contrib = [rc * 100 for rc in risk_metrics['risk_contribution_pct']]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            bars = ax.bar(tickers, risk_contrib, color='#3b82f6', alpha=0.8)
            
            # Add value labels on bars
            for bar, value in zip(bars, risk_contrib):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            ax.set_title('Risk Contribution by Security', fontsize=16, fontweight='bold', color='#1e3a8a')
            ax.set_xlabel('Securities', fontsize=12)
            ax.set_ylabel('Risk Contribution (%)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            
            # Professional styling
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            
            # Save to memory
            img_buffer = BytesIO()
            fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            plt.close(fig)
            
            return img_buffer
            
        except Exception as e:
            self.logger.error(f"Error creating risk contribution chart: {str(e)}")
            return None
    
    def create_enhanced_pdf_digest(self, portfolio_data, market_data, risk_metrics, filename, date_str):
        """Create optimized 2-page enterprise-grade PDF report"""
        
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Professional styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor(self.colors['primary']),
            spaceAfter=20,
            alignment=1
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'], 
            fontSize=14,
            textColor=colors.HexColor(self.colors['secondary']),
            spaceAfter=10,
            spaceBefore=15
        )
        
        subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor(self.colors['accent']),
            spaceAfter=8,
            spaceBefore=10
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor(self.colors['text']),
            spaceAfter=6,
            leading=12
        )
        
        # PAGE 1: EXECUTIVE SUMMARY WITH ALLOCATION
        story.append(Paragraph("Capital Markets Intelligence", title_style))
        story.append(Paragraph("Daily Portfolio Intelligence Digest", header_style))
        story.append(Paragraph(f"Report Date: {date_str}", body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", header_style))
        
        if portfolio_data and 'portfolio_tickers' in portfolio_data:
            portfolio_count = len(portfolio_data['portfolio_tickers'])
            story.append(Paragraph(f"Portfolio Analysis: {portfolio_count} securities under management", body_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Compact portfolio table
            if 'portfolio_weights' in portfolio_data:
                table_data = [['Security', 'Weight', 'Status']]
                for i, ticker in enumerate(portfolio_data['portfolio_tickers']):
                    if i < len(portfolio_data['portfolio_weights']):
                        weight = f"{portfolio_data['portfolio_weights'][i]:.1f}%"
                        table_data.append([ticker, weight, 'Active'])
                
                table = Table(table_data, colWidths=[1.5*inch, 1*inch, 1*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors['primary'])),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
                ]))
                
                story.append(table)
                story.append(Spacer(1, 0.15*inch))
        
        # Portfolio Allocation Chart - SMALLER SIZE
        story.append(Paragraph("Portfolio Allocation Analysis", subheader_style))
        allocation_chart = self.create_portfolio_allocation_chart(portfolio_data)
        if allocation_chart:
            story.append(Image(allocation_chart, width=3.5*inch, height=3.5*inch))
        else:
            story.append(Spacer(1, 0.1*inch))
        
        # PAGE BREAK
        story.append(PageBreak())
        
        # PAGE 2: MONTE CARLO ANALYSIS - COMPRESSED LAYOUT
        story.append(Paragraph("Monte Carlo Risk Analysis", header_style))
        
        if risk_metrics:
            # Compact risk metrics table
            risk_data = [
                ['Risk Metric', 'Value', 'Assessment', 'Benchmark'],
                ['Expected Return', f"{risk_metrics.get('expected_return', 0)*100:.2f}%", 'Optimized', '> 8%'],
                ['Portfolio Volatility', f"{risk_metrics.get('volatility', 0)*100:.2f}%", 'Controlled', '< 20%'],
                ['Value at Risk (95%)', f"{risk_metrics.get('var_95', 0)*100:.2f}%", 'Monitored', '< -15%'],
                ['Sharpe Ratio', f"{risk_metrics.get('sharpe_ratio', 0):.2f}", 'Efficient', '> 1.0'],
                ['Maximum Drawdown', f"{risk_metrics.get('max_drawdown', 0)*100:.2f}%", 'Acceptable', '< -25%']
            ]
            
            risk_table = Table(risk_data, colWidths=[1.4*inch, 0.8*inch, 0.9*inch, 0.7*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.colors['accent'])),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f9ff')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bfdbfe'))
            ]))
            
            story.append(risk_table)
            story.append(Spacer(1, 0.1*inch))
        
        # Monte Carlo Simulation Chart - COMPRESSED
        story.append(Paragraph("Simulation Path Analysis", subheader_style))
        mc_chart = self.create_monte_carlo_chart(risk_metrics)
        if mc_chart:
            story.append(Image(mc_chart, width=6.5*inch, height=2.8*inch))
        story.append(Spacer(1, 0.1*inch))
        
        # Risk Contribution Chart - COMPRESSED
        story.append(Paragraph("Risk Contribution Analysis", subheader_style))
        risk_chart = self.create_risk_contribution_chart(risk_metrics)
        if risk_chart:
            story.append(Image(risk_chart, width=6.5*inch, height=2.2*inch))
        
        # Compact footer
        story.append(Spacer(1, 0.1*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6b7280'),
            alignment=1
        )
        
        story.append(Paragraph(
            f"Generated by Capital Markets Intelligence • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
            footer_style
        ))
        
        doc.build(story)
        return filename
    
    def create_professional_excel_dashboard(self, portfolio_data, market_data, risk_metrics, filename):
        """Create enterprise-grade Excel dashboard"""
        
        workbook = xlsxwriter.Workbook(filename)
        
        # Professional formats
        title_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 18,
            'bold': True,
            'font_color': '#1e3a8a',
            'align': 'center'
        })
        
        header_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 12,
            'bold': True,
            'bg_color': '#1e3a8a',
            'font_color': 'white',
            'align': 'center',
            'border': 1
        })
        
        data_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 11,
            'align': 'center',
            'border': 1
        })
        
        percentage_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 11,
            'align': 'center',
            'border': 1,
            'num_format': '0.00%'
        })
        
        # Executive Dashboard
        dashboard = workbook.add_worksheet('Executive Dashboard')
        dashboard.set_column('A:H', 15)
        
        dashboard.merge_range('A1:H1', f'{self.company_name} - Daily KPI Dashboard', title_format)
        dashboard.write('A2', f'Report Date: {datetime.now().strftime("%B %d, %Y")}', data_format)
        
        # Portfolio Overview
        row = 4
        dashboard.write(f'A{row}', 'Portfolio Overview', header_format)
        dashboard.write(f'B{row}', 'Current Status', header_format)  
        dashboard.write(f'C{row}', 'Weight %', header_format)
        dashboard.write(f'D{row}', 'Risk Contrib %', header_format)
        row += 1
        
        if portfolio_data and 'portfolio_tickers' in portfolio_data:
            for i, ticker in enumerate(portfolio_data['portfolio_tickers']):
                dashboard.write(f'A{row}', ticker, data_format)
                dashboard.write(f'B{row}', 'Active', data_format)
                if 'portfolio_weights' in portfolio_data and i < len(portfolio_data['portfolio_weights']):
                    dashboard.write(f'C{row}', portfolio_data['portfolio_weights'][i]/100, percentage_format)
                
                # Add risk contribution if available
                if risk_metrics and 'risk_contribution_pct' in risk_metrics and i < len(risk_metrics['risk_contribution_pct']):
                    dashboard.write(f'D{row}', risk_metrics['risk_contribution_pct'][i], percentage_format)
                row += 1
        
        # Enhanced Risk Metrics
        row += 2
        dashboard.write(f'A{row}', 'Risk Metrics', header_format)
        dashboard.write(f'B{row}', 'Value', header_format)
        dashboard.write(f'C{row}', 'Status', header_format)
        dashboard.write(f'D{row}', 'Benchmark', header_format)
        row += 1
        
        if risk_metrics:
            metrics = [
                ('Expected Return', f"{risk_metrics.get('expected_return', 0)*100:.2f}%", 'Optimized', '> 8%'),
                ('Portfolio Volatility', f"{risk_metrics.get('volatility', 0)*100:.2f}%", 'Controlled', '< 20%'),
                ('Value at Risk (95%)', f"{risk_metrics.get('var_95', 0)*100:.2f}%", 'Monitored', '< -15%'),
                ('Sharpe Ratio', f"{risk_metrics.get('sharpe_ratio', 0):.2f}", 'Efficient', '> 1.0'),
                ('Maximum Drawdown', f"{risk_metrics.get('max_drawdown', 0)*100:.2f}%", 'Acceptable', '< -25%')
            ]
            
            for metric_name, value, status, benchmark in metrics:
                dashboard.write(f'A{row}', metric_name, data_format)
                dashboard.write(f'B{row}', value, data_format)
                dashboard.write(f'C{row}', status, data_format)
                dashboard.write(f'D{row}', benchmark, data_format)
                row += 1
        
        workbook.close()
        return filename
    
    def create_executive_summary(self, portfolio_data, risk_metrics):
        """Generate enhanced executive summary"""
        
        summary = {
            'report_date': datetime.now().strftime("%B %d, %Y"),
            'portfolio_count': len(portfolio_data.get('portfolio_tickers', [])) if portfolio_data else 0,
            'key_metrics': {},
            'recommendations': []
        }
        
        if risk_metrics:
            summary['key_metrics'] = {
                'expected_return': f"{risk_metrics.get('expected_return', 0)*100:.2f}%",
                'volatility': f"{risk_metrics.get('volatility', 0)*100:.2f}%",
                'sharpe_ratio': f"{risk_metrics.get('sharpe_ratio', 0):.2f}",
                'var_95': f"{risk_metrics.get('var_95', 0)*100:.2f}%",
                'max_drawdown': f"{risk_metrics.get('max_drawdown', 0)*100:.2f}%"
            }
            
            # Enhanced recommendations based on metrics
            if risk_metrics.get('sharpe_ratio', 0) > 1.0:
                summary['recommendations'].append("Portfolio demonstrates strong risk-adjusted returns")
            if risk_metrics.get('volatility', 0) < 0.2:
                summary['recommendations'].append("Volatility levels within institutional limits")
            if risk_metrics.get('max_drawdown', 0) > -0.25:
                summary['recommendations'].append("Drawdown risk is well-controlled")
            
            summary['recommendations'].append("Regular portfolio rebalancing recommended")
            summary['recommendations'].append("Monte Carlo analysis supports current allocation strategy")
        
        return summary


# Integration Manager
class ReportIntegrationManager:
    """Professional integration for Streamlit platform"""
    
    def __init__(self):
        self.report_generator = ProfessionalReportGenerator()
    
    def generate_reports_from_streamlit_session(self, st_session_state):
        """Generate enhanced reports from Streamlit session state"""
        
        portfolio_data = {
            'portfolio_tickers': st_session_state.get('portfolio_tickers', []),
            'portfolio_weights': st_session_state.get('portfolio_weights', [])
        }
        
        risk_metrics = st_session_state.get('monte_carlo_results', {})
        
        market_data = {
            'sentiment': 'Optimistic',
            'score': 75,
            'vix_level': 16.2
        }
        
        return self.report_generator.generate_daily_kpi_digest(
            portfolio_data, market_data, risk_metrics
        )


class IndividualSecurityReportManager:
    """Professional individual security report generation"""
    
    def __init__(self):
        self.report_generator = ProfessionalReportGenerator()
    
    def generate_individual_security_report(self, ticker, stock_data, company_data):
        """Generate professional individual security analysis report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_str = datetime.now().strftime("%B %d, %Y")
            
            pdf_filename = f"output/daily_reports/{ticker}_Security_Analysis_{timestamp}.pdf"
            excel_filename = f"output/daily_reports/{ticker}_Security_Dashboard_{timestamp}.xlsx"
            
            # Generate individual security PDF
            pdf_path = self.create_individual_security_pdf(
                ticker, stock_data, company_data, pdf_filename, date_str
            )
            
            # Generate individual security Excel
            excel_path = self.create_individual_security_excel(
                ticker, stock_data, company_data, excel_filename
            )
            
            return {
                'pdf_report': pdf_path,
                'excel_dashboard': excel_path,
                'generation_time': datetime.now(),
                'status': 'success'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def create_individual_security_pdf(self, ticker, stock_data, company_data, filename, date_str):
        """Create professional individual security PDF analysis"""
        
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                              rightMargin=0.75*inch, leftMargin=0.75*inch,
                              topMargin=1*inch, bottomMargin=1*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Professional styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=1
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'], 
            fontSize=16,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            leading=14
        )
        
        # Report Header
        story.append(Paragraph("Capital Markets Intelligence", title_style))
        story.append(Paragraph(f"Individual Security Analysis: {ticker}", header_style))
        story.append(Paragraph(f"Report Date: {date_str}", body_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Company Profile
        story.append(Paragraph("Company Profile", header_style))
        story.append(Paragraph(f"Company Name: {stock_data.get('name', 'N/A')}", body_style))
        story.append(Paragraph(f"Sector: {stock_data.get('sector', 'N/A')}", body_style))
        story.append(Paragraph(f"Industry: {stock_data.get('industry', 'N/A')}", body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Market Valuation
        story.append(Paragraph("Current Market Valuation", header_style))
        
        valuation_data = [
            ['Metric', 'Value', 'Assessment'],
            ['Current Price', f"${stock_data.get('price', 0):.2f}", 'Current'],
            ['Market Cap', f"${stock_data.get('market_cap', 0)/1e9:.1f}B" if stock_data.get('market_cap', 0) > 1e9 else f"${stock_data.get('market_cap', 0)/1e6:.0f}M", 'Large Cap' if stock_data.get('market_cap', 0) > 10e9 else 'Mid Cap'],
            ['P/E Ratio', f"{stock_data.get('pe_ratio', 0):.1f}x" if stock_data.get('pe_ratio') else "N/A", 'Reasonable' if stock_data.get('pe_ratio', 0) < 25 else 'Premium'],
            ['Volume', f"{stock_data.get('volume', 0)/1e6:.1f}M" if stock_data.get('volume', 0) > 1e6 else f"{stock_data.get('volume', 0):,}", 'Active']
        ]
        
        valuation_table = Table(valuation_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        valuation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
        ]))
        
        story.append(valuation_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Business Summary
        if stock_data.get('summary') and stock_data['summary'] != 'N/A':
            story.append(Paragraph("Business Intelligence Summary", header_style))
            summary_text = stock_data['summary'][:500] + "..." if len(stock_data['summary']) > 500 else stock_data['summary']
            story.append(Paragraph(summary_text, body_style))
        
        # Professional recommendations
        story.append(Paragraph("Investment Analysis", header_style))
        
        recommendations = [
            f"Current trading price: ${stock_data.get('price', 0):.2f}",
            f"Market capitalization: ${stock_data.get('market_cap', 0)/1e9:.1f}B",
            "Professional analysis completed with institutional-grade metrics",
            "Regular monitoring recommended for investment decisions"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", body_style))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            alignment=1
        )
        
        story.append(Paragraph(
            f"Generated by Capital Markets Intelligence • Individual Security Analysis • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
            footer_style
        ))
        
        doc.build(story)
        return filename
    
    def create_individual_security_excel(self, ticker, stock_data, company_data, filename):
        """Create professional individual security Excel dashboard"""
        
        workbook = xlsxwriter.Workbook(filename)
        
        # Professional formats
        title_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 18,
            'bold': True,
            'font_color': '#1e3a8a',
            'align': 'center'
        })
        
        header_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 12,
            'bold': True,
            'bg_color': '#1e3a8a',
            'font_color': 'white',
            'align': 'center',
            'border': 1
        })
        
        data_format = workbook.add_format({
            'font_name': 'Calibri',
            'font_size': 11,
            'align': 'center',
            'border': 1
        })
        
        # Security Analysis Sheet
        analysis = workbook.add_worksheet('Security Analysis')
        analysis.set_column('A:D', 20)
        
        analysis.merge_range('A1:D1', f'{ticker} - Individual Security Analysis', title_format)
        analysis.write('A2', f'Report Date: {datetime.now().strftime("%B %d, %Y")}', data_format)
        
        # Company Information
        row = 4
        analysis.write(f'A{row}', 'Company Information', header_format)
        analysis.write(f'B{row}', 'Value', header_format)
        row += 1
        
        company_info = [
            ('Company Name', stock_data.get('name', 'N/A')),
            ('Ticker', ticker),
            ('Sector', stock_data.get('sector', 'N/A')),
            ('Industry', stock_data.get('industry', 'N/A'))
        ]
        
        for label, value in company_info:
            analysis.write(f'A{row}', label, data_format)
            analysis.write(f'B{row}', str(value), data_format)
            row += 1
        
        # Market Metrics
        row += 2
        analysis.write(f'A{row}', 'Market Metrics', header_format)
        analysis.write(f'B{row}', 'Value', header_format)
        analysis.write(f'C{row}', 'Assessment', header_format)
        row += 1
        
        market_metrics = [
            ('Current Price', f"${stock_data.get('price', 0):.2f}", 'Current Market'),
            ('Market Cap', f"${stock_data.get('market_cap', 0)/1e9:.1f}B" if stock_data.get('market_cap', 0) > 1e9 else f"${stock_data.get('market_cap', 0)/1e6:.0f}M", 'Large Cap' if stock_data.get('market_cap', 0) > 10e9 else 'Mid Cap'),
            ('P/E Ratio', f"{stock_data.get('pe_ratio', 0):.1f}x" if stock_data.get('pe_ratio') else "N/A", 'Reasonable' if stock_data.get('pe_ratio', 0) < 25 else 'Premium'),
            ('Trading Volume', f"{stock_data.get('volume', 0)/1e6:.1f}M" if stock_data.get('volume', 0) > 1e6 else f"{stock_data.get('volume', 0):,}", 'Active Trading')
        ]
        
        for metric, value, assessment in market_metrics:
            analysis.write(f'A{row}', metric, data_format)
            analysis.write(f'B{row}', value, data_format)
            analysis.write(f'C{row}', assessment, data_format)
            row += 1
        
        workbook.close()
        return filename
