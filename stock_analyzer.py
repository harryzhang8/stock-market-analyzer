import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
import warnings
import logging

warnings.filterwarnings ( 'ignore' )

# Configure matplotlib for better output
plt.style.use ( 'seaborn-v0_8' )

# Configure logging
logging.basicConfig ( level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s' )
logger = logging.getLogger ( __name__ )


class StockAnalyzer:
    """
    A comprehensive stock market analysis tool for technical analysis and visualization.

    This class provides functionality to:
    - Fetch historical stock data
    - Calculate technical indicators
    - Perform trend analysis
    - Generate visualizations
    - Create detailed analysis reports
    """

    def __init__(self, custom_stocks: Optional[Dict[str, str]] = None):
        """
        Initialize the StockAnalyzer with default or custom stock symbols.

        Args:
            custom_stocks: Dictionary of {symbol: description} for custom analysis
        """
        self.stocks = custom_stocks if custom_stocks else {
            'AAPL': 'Apple Inc. - Technology',
            'MSFT': 'Microsoft Corporation - Technology',
            'AMZN': 'Amazon.com Inc. - Consumer Discretionary',
            'TSLA': 'Tesla Inc. - Consumer Discretionary',
            'NVDA': 'NVIDIA Corporation - Technology',
            'JNJ': 'Johnson & Johnson - Healthcare',
            'JPM': 'JPMorgan Chase & Co. - Financial',
            'XOM': 'Exxon Mobil Corporation - Energy',
            'PG': 'Procter & Gamble Co. - Consumer Staples',
            'WMT': 'Walmart Inc. - Consumer Staples',
            'AMT': 'American Tower Corporation - Real Estate'
        }

        self.stock_data: Dict[str, pd.DataFrame] = {}
        self.analysis_results: Dict[str, Dict] = {}

    def fetch_stock_data(self, period: str = '5y') -> bool:
        """
        Fetch historical stock data for all symbols.

        Args:
            period: Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info ( "Fetching stock data..." )

        successful_fetches = 0
        for symbol in self.stocks.keys ():
            try:
                ticker = yf.Ticker ( symbol )
                data = ticker.history ( period=period )

                if not data.empty:
                    self.stock_data[symbol] = data
                    logger.info ( f"✓ {symbol}: {len ( data )} records fetched successfully" )
                    successful_fetches += 1
                else:
                    logger.warning ( f"✗ {symbol}: No data retrieved" )

            except Exception as e:
                logger.error ( f"✗ {symbol}: Error fetching data - {str ( e )}" )

        logger.info ( f"Data fetching complete: {successful_fetches}/{len ( self.stocks )} stocks retrieved" )
        return successful_fetches > 0

    def clean_and_preprocess_data(self) -> None:
        """
        Clean and preprocess the fetched stock data.

        This method handles:
        - Missing value imputation
        - Outlier detection and smoothing
        - Data validation
        """
        logger.info ( "Starting data cleaning and preprocessing..." )

        for symbol, data in self.stock_data.items ():
            # Check for missing values
            missing_values = data.isnull ().sum ()
            if missing_values.sum () > 0:
                logger.info ( f"{symbol}: Found {missing_values.sum ()} missing values" )

            # Forward fill missing values, then backward fill if needed
            data_cleaned = data.fillna ( method='ffill' ).fillna ( method='bfill' )

            # Detect price anomalies (changes > 50%)
            price_changes = data_cleaned['Close'].pct_change ().abs ()
            outliers = price_changes > 0.5

            if outliers.sum () > 0:
                logger.info ( f"{symbol}: Found {outliers.sum ()} potential outliers" )
                # Smooth outliers using rolling mean
                data_cleaned.loc[outliers, 'Close'] = (
                    data_cleaned['Close'].rolling ( window=3, center=True ).mean ()
                )

            self.stock_data[symbol] = data_cleaned

        logger.info ( "Data cleaning completed" )

    def calculate_technical_indicators(self) -> None:
        """
        Calculate comprehensive technical indicators for all stocks.

        Indicators calculated:
        - Moving Averages (50, 200 day)
        - RSI (Relative Strength Index)
        - MACD (Moving Average Convergence Divergence)
        - Bollinger Bands
        - Price volatility
        """
        logger.info ( "Calculating technical indicators..." )

        for symbol, data in self.stock_data.items ():
            # Moving Averages
            data['MA_50'] = data['Close'].rolling ( window=50 ).mean ()
            data['MA_200'] = data['Close'].rolling ( window=200 ).mean ()

            # RSI Calculation
            delta = data['Close'].diff ()
            gain = delta.where ( delta > 0, 0 ).rolling ( window=14 ).mean ()
            loss = (-delta.where ( delta < 0, 0 )).rolling ( window=14 ).mean ()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))

            # MACD Calculation
            exp12 = data['Close'].ewm ( span=12 ).mean ()
            exp26 = data['Close'].ewm ( span=26 ).mean ()
            data['MACD'] = exp12 - exp26
            data['MACD_Signal'] = data['MACD'].ewm ( span=9 ).mean ()
            data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']

            # Bollinger Bands
            data['BB_Middle'] = data['Close'].rolling ( window=20 ).mean ()
            bb_std = data['Close'].rolling ( window=20 ).std ()
            data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
            data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)

            # Price Volatility (30-day)
            data['Volatility'] = data['Close'].rolling ( window=30 ).std ()

            # Price Change Percentage
            data['Price_Change_Pct'] = data['Close'].pct_change () * 100

            logger.info ( f"✓ {symbol}: Technical indicators calculated" )

        logger.info ( "Technical indicators calculation completed" )

    def analyze_trends(self) -> None:
        """
        Perform comprehensive trend analysis for all stocks.

        Analysis includes:
        - Moving average signals
        - RSI overbought/oversold conditions
        - MACD momentum signals
        - Bollinger band position
        - Overall recommendation scoring
        """
        logger.info ( "Starting trend analysis..." )

        for symbol, data in self.stock_data.items ():
            latest = data.iloc[-1]
            analysis = self._analyze_single_stock ( latest )
            analysis['current_price'] = latest['Close']
            analysis['volatility'] = latest['Volatility']

            self.analysis_results[symbol] = analysis

        logger.info ( "Trend analysis completed" )

    def _analyze_single_stock(self, latest_data: pd.Series) -> Dict:
        """
        Analyze a single stock's latest data point.

        Args:
            latest_data: Latest data point for the stock

        Returns:
            Dict: Analysis results including signals and recommendations
        """
        # Moving Average Signal
        ma_signal = self._get_ma_signal ( latest_data )

        # RSI Signal
        rsi_value = latest_data['RSI']
        rsi_signal = self._get_rsi_signal ( rsi_value )

        # MACD Signal
        macd_signal = self._get_macd_signal ( latest_data )

        # Bollinger Bands Signal
        bb_signal = self._get_bb_signal ( latest_data )

        # Calculate composite score (-3 to +3)
        score = self._calculate_composite_score ( ma_signal, rsi_signal, macd_signal )

        # Generate recommendation
        recommendation = self._get_recommendation ( score )

        return {
            'ma_signal': ma_signal,
            'rsi_value': rsi_value,
            'rsi_signal': rsi_signal,
            'macd_signal': macd_signal,
            'bb_signal': bb_signal,
            'score': score,
            'recommendation': recommendation
        }

    def _get_ma_signal(self, data: pd.Series) -> str:
        """Generate moving average signal."""
        close, ma50, ma200 = data['Close'], data['MA_50'], data['MA_200']

        if close > ma50 > ma200:
            return "Strong Bullish"
        elif close > ma50:
            return "Bullish"
        elif close < ma50 < ma200:
            return "Strong Bearish"
        else:
            return "Bearish"

    def _get_rsi_signal(self, rsi: float) -> str:
        """Generate RSI signal."""
        if rsi > 70:
            return "Overbought"
        elif rsi < 30:
            return "Oversold"
        else:
            return "Neutral"

    def _get_macd_signal(self, data: pd.Series) -> str:
        """Generate MACD signal."""
        return "Bullish" if data['MACD'] > data['MACD_Signal'] else "Bearish"

    def _get_bb_signal(self, data: pd.Series) -> str:
        """Generate Bollinger Bands signal."""
        close = data['Close']
        if close > data['BB_Upper']:
            return "Above upper band - potentially overbought"
        elif close < data['BB_Lower']:
            return "Below lower band - potentially oversold"
        else:
            return "Within normal range"

    def _calculate_composite_score(self, ma_signal: str, rsi_signal: str, macd_signal: str) -> int:
        """Calculate composite score based on all signals."""
        score = 0

        # MA Score
        if "Bullish" in ma_signal:
            score += 2 if "Strong" in ma_signal else 1
        elif "Bearish" in ma_signal:
            score -= 2 if "Strong" in ma_signal else 1

        # RSI Score
        if rsi_signal == "Overbought":
            score -= 1
        elif rsi_signal == "Oversold":
            score += 1

        # MACD Score
        score += 1 if macd_signal == "Bullish" else -1

        return max ( -3, min ( 3, score ) )

    def _get_recommendation(self, score: int) -> str:
        """Generate investment recommendation based on composite score."""
        recommendations = {
            3: "Strong Buy", 2: "Strong Buy",
            1: "Buy", 0: "Hold",
            -1: "Sell", -2: "Strong Sell", -3: "Strong Sell"
        }
        return recommendations.get ( score, "Hold" )

    def create_visualizations(self) -> None:
        """
        Generate comprehensive visualizations for analysis.

        Creates:
        - Individual stock charts with technical indicators
        - Comparative analysis charts
        - Correlation heatmap
        """
        logger.info ( "Generating visualizations..." )

        # Create individual stock charts
        for symbol, data in self.stock_data.items ():
            self._create_stock_chart ( symbol, data )

        # Create comparison charts
        self._create_comparison_charts ()

        # Create correlation analysis
        self._create_correlation_analysis ()

        logger.info ( "Visualization generation completed" )

    def _create_stock_chart(self, symbol: str, data: pd.DataFrame) -> None:
        """Create detailed technical analysis chart for a single stock."""
        fig = make_subplots (
            rows=4, cols=1,
            shared_xaxis=True,
            vertical_spacing=0.05,
            subplot_titles=(
                f'{symbol} - {self.stocks[symbol]} Price Action',
                'RSI (Relative Strength Index)',
                'MACD Indicator',
                'Volume'
            ),
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )

        # Main price chart with candlesticks
        fig.add_trace (
            go.Candlestick (
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price',
                showlegend=False
            ),
            row=1, col=1
        )

        # Moving averages
        fig.add_trace (
            go.Scatter ( x=data.index, y=data['MA_50'], name='MA50',
                         line=dict ( color='orange', width=1 ) ),
            row=1, col=1
        )

        fig.add_trace (
            go.Scatter ( x=data.index, y=data['MA_200'], name='MA200',
                         line=dict ( color='red', width=1 ) ),
            row=1, col=1
        )

        # Bollinger Bands
        fig.add_trace (
            go.Scatter ( x=data.index, y=data['BB_Upper'], name='BB Upper',
                         line=dict ( color='gray', dash='dash', width=1 ) ),
            row=1, col=1
        )

        fig.add_trace (
            go.Scatter ( x=data.index, y=data['BB_Lower'], name='BB Lower',
                         line=dict ( color='gray', dash='dash', width=1 ) ),
            row=1, col=1
        )

        # RSI
        fig.add_trace (
            go.Scatter ( x=data.index, y=data['RSI'], name='RSI',
                         line=dict ( color='purple' ) ),
            row=2, col=1
        )
        fig.add_hline ( y=70, line_dash="dash", line_color="red", row=2, col=1 )
        fig.add_hline ( y=30, line_dash="dash", line_color="green", row=2, col=1 )

        # MACD
        fig.add_trace (
            go.Scatter ( x=data.index, y=data['MACD'], name='MACD',
                         line=dict ( color='blue' ) ),
            row=3, col=1
        )
        fig.add_trace (
            go.Scatter ( x=data.index, y=data['MACD_Signal'], name='Signal',
                         line=dict ( color='red' ) ),
            row=3, col=1
        )
        fig.add_trace (
            go.Bar ( x=data.index, y=data['MACD_Histogram'], name='Histogram',
                     marker_color='lightblue' ),
            row=3, col=1
        )

        # Volume
        fig.add_trace (
            go.Bar ( x=data.index, y=data['Volume'], name='Volume',
                     marker_color='lightgreen' ),
            row=4, col=1
        )

        fig.update_layout (
            title=f'{symbol} - Technical Analysis Dashboard',
            xaxis_title='Date',
            height=800,
            showlegend=True,
            template='plotly_white'
        )

        fig.write_html ( f'{symbol}_technical_analysis.html' )

    def _create_comparison_charts(self) -> None:
        """Create comparative analysis charts for all stocks."""
        fig, axes = plt.subplots ( 2, 2, figsize=(16, 12) )

        # Normalized price comparison
        ax1 = axes[0, 0]
        for symbol, data in self.stock_data.items ():
            normalized_price = (data['Close'] / data['Close'].iloc[0]) * 100
            ax1.plot ( data.index, normalized_price, label=symbol, alpha=0.8, linewidth=2 )
        ax1.set_title ( 'Normalized Price Comparison (Base = 100)', fontsize=14, fontweight='bold' )
        ax1.set_ylabel ( 'Normalized Price' )
        ax1.legend ( bbox_to_anchor=(1.05, 1), loc='upper left' )
        ax1.grid ( True, alpha=0.3 )

        # Volatility comparison
        ax2 = axes[0, 1]
        volatilities = [data['Volatility'].iloc[-1] for data in self.stock_data.values ()]
        symbols = list ( self.stock_data.keys () )
        colors = plt.cm.viridis ( np.linspace ( 0, 1, len ( symbols ) ) )
        bars = ax2.bar ( symbols, volatilities, color=colors, alpha=0.8 )
        ax2.set_title ( '30-Day Volatility Comparison', fontsize=14, fontweight='bold' )
        ax2.set_ylabel ( 'Volatility' )
        ax2.tick_params ( axis='x', rotation=45 )

        # Current RSI comparison
        ax3 = axes[1, 0]
        current_rsi = [data['RSI'].iloc[-1] for data in self.stock_data.values ()]
        bars = ax3.bar ( symbols, current_rsi, color=colors, alpha=0.8 )
        ax3.axhline ( y=70, color='r', linestyle='--', alpha=0.7, label='Overbought' )
        ax3.axhline ( y=30, color='g', linestyle='--', alpha=0.7, label='Oversold' )
        ax3.set_title ( 'Current RSI Comparison', fontsize=14, fontweight='bold' )
        ax3.set_ylabel ( 'RSI Value' )
        ax3.tick_params ( axis='x', rotation=45 )
        ax3.legend ()

        # Annualized returns comparison
        ax4 = axes[1, 1]
        annual_returns = []
        for symbol, data in self.stock_data.items ():
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]
            days = (data.index[-1] - data.index[0]).days
            annual_return = ((end_price / start_price) ** (365 / days) - 1) * 100
            annual_returns.append ( annual_return )

        colors_return = ['green' if x > 0 else 'red' for x in annual_returns]
        bars = ax4.bar ( symbols, annual_returns, color=colors_return, alpha=0.8 )
        ax4.set_title ( 'Annualized Returns Comparison', fontsize=14, fontweight='bold' )
        ax4.set_ylabel ( 'Annualized Return (%)' )
        ax4.tick_params ( axis='x', rotation=45 )
        ax4.axhline ( y=0, color='black', linestyle='-', alpha=0.5 )

        plt.tight_layout ()
        plt.savefig ( 'stock_comparison_analysis.png', dpi=300, bbox_inches='tight' )
        plt.close ()

    def _create_correlation_analysis(self) -> pd.DataFrame:
        """Create correlation analysis heatmap."""
        # Build price matrix
        price_data = pd.DataFrame ()
        for symbol, data in self.stock_data.items ():
            price_data[symbol] = data['Close']

        # Calculate correlation matrix
        correlation_matrix = price_data.corr ()

        # Create heatmap
        plt.figure ( figsize=(12, 10) )
        mask = np.triu ( np.ones_like ( correlation_matrix, dtype=bool ) )
        sns.heatmap (
            correlation_matrix,
            mask=mask,
            annot=True,
            cmap='RdYlBu_r',
            center=0,
            square=True,
            cbar_kws={"shrink": .8},
            fmt='.2f',
            annot_kws={'size': 10}
        )
        plt.title ( 'Stock Price Correlation Matrix', fontsize=16, fontweight='bold', pad=20 )
        plt.tight_layout ()
        plt.savefig ( 'correlation_heatmap.png', dpi=300, bbox_inches='tight' )
        plt.close ()

        return correlation_matrix

    def generate_report(self) -> str:
        """
        Generate comprehensive analysis report.

        Returns:
            str: Formatted analysis report
        """
        logger.info ( "Generating analysis report..." )

        report_lines = []
        report_lines.extend ( [
            "=" * 80,
            "COMPREHENSIVE STOCK MARKET ANALYSIS REPORT",
            "=" * 80,
            f"Report Generated: {datetime.now ().strftime ( '%Y-%m-%d %H:%M:%S' )}",
            f"Stocks Analyzed: {len ( self.stock_data )}",
            f"Data Period: 5 Years Historical Data",
            ""
        ] )

        # Executive Summary
        buy_signals = sum ( 1 for analysis in self.analysis_results.values ()
                            if "Buy" in analysis['recommendation'] )
        sell_signals = sum ( 1 for analysis in self.analysis_results.values ()
                             if "Sell" in analysis['recommendation'] )
        hold_signals = sum ( 1 for analysis in self.analysis_results.values ()
                             if analysis['recommendation'] == "Hold" )

        report_lines.extend ( [
            "EXECUTIVE SUMMARY",
            "-" * 40,
            f"Buy Signals: {buy_signals} stocks",
            f"Sell Signals: {sell_signals} stocks",
            f"Hold Signals: {hold_signals} stocks",
            ""
        ] )

        # Individual Stock Analysis
        report_lines.extend ( [
            "INDIVIDUAL STOCK ANALYSIS",
            "-" * 40
        ] )

        for symbol, analysis in self.analysis_results.items ():
            report_lines.extend ( [
                f"\n{symbol} - {self.stocks[symbol]}",
                f"Current Price: ${analysis['current_price']:.2f}",
                f"Moving Average Signal: {analysis['ma_signal']}",
                f"RSI: {analysis['rsi_value']:.2f} ({analysis['rsi_signal']})",
                f"MACD Signal: {analysis['macd_signal']}",
                f"Bollinger Bands: {analysis['bb_signal']}",
                f"30-Day Volatility: {analysis['volatility']:.2f}",
                f"Composite Score: {analysis['score']}/3",
                f"Recommendation: {analysis['recommendation']}",
                "-" * 60
            ] )

        # Sector Analysis
        report_lines.extend ( [
            "\nSECTOR ANALYSIS",
            "-" * 40
        ] )

        sectors = {}
        for symbol, description in self.stocks.items ():
            if ' - ' in description:
                sector = description.split ( ' - ' )[1]
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append ( symbol )

        for sector, symbols in sectors.items ():
            if len ( symbols ) > 1:
                sector_scores = [self.analysis_results[symbol]['score'] for symbol in symbols]
                avg_score = sum ( sector_scores ) / len ( sector_scores )
                report_lines.extend ( [
                    f"{sector} Sector Average Score: {avg_score:.1f}",
                    f"Stocks: {', '.join ( symbols )}",
                    ""
                ] )

        # Risk Disclaimer
        report_lines.extend ( [
            "RISK DISCLAIMER",
            "-" * 40,
            "1. This analysis is based on historical data and technical indicators",
            "2. Past performance does not guarantee future results",
            "3. All investments carry risk of capital loss",
            "4. Consult with financial advisors before making investment decisions",
            "5. Technical analysis should be combined with fundamental analysis",
            ""
        ] )

        # Methodology
        report_lines.extend ( [
            "METHODOLOGY",
            "-" * 40,
            "Moving Averages: 50-day and 200-day for trend identification",
            "RSI: 14-period Relative Strength Index (0-100 scale)",
            "MACD: Moving Average Convergence Divergence for momentum",
            "Bollinger Bands: 20-period MA ± 2 standard deviations",
            "Volatility: 30-day rolling standard deviation of returns"
        ] )

        report_text = '\n'.join ( report_lines )

        # Save report
        with open ( 'stock_analysis_report.txt', 'w', encoding='utf-8' ) as f:
            f.write ( report_text )

        logger.info ( "Analysis report saved as 'stock_analysis_report.txt'" )
        return report_text

    def run_complete_analysis(self) -> str:
        """
        Execute the complete analysis workflow.

        Returns:
            str: Analysis report
        """
        logger.info ( "Starting comprehensive stock analysis..." )
        logger.info ( "=" * 80 )

        try:
            # Execute analysis pipeline
            if not self.fetch_stock_data ():
                raise Exception ( "Failed to fetch stock data" )

            self.clean_and_preprocess_data ()
            self.calculate_technical_indicators ()
            self.analyze_trends ()
            self.create_visualizations ()
            report = self.generate_report ()

            logger.info ( "=" * 80 )
            logger.info ( "Analysis completed successfully!" )
            logger.info ( "Generated files:" )
            logger.info ( "1. stock_analysis_report.txt - Detailed analysis report" )
            logger.info ( "2. stock_comparison_analysis.png - Comparative charts" )
            logger.info ( "3. correlation_heatmap.png - Correlation analysis" )
            logger.info ( "4. [SYMBOL]_technical_analysis.html - Individual stock charts" )
            logger.info ( "=" * 80 )

            return report

        except Exception as e:
            logger.error ( f"Analysis failed: {str ( e )}" )
            raise

    def print_summary(self) -> None:
        """Print a formatted summary of recommendations."""
        print ( "\n" + "=" * 80 )
        print ( "INVESTMENT RECOMMENDATIONS SUMMARY" )
        print ( "=" * 80 )
        print ( f"{'Symbol':<8} {'Company':<20} {'Recommendation':<12} {'Price':<10} {'RSI':<6} {'Score':<6}" )
        print ( "-" * 80 )

        for symbol, analysis in self.analysis_results.items ():
            company_name = self.stocks[symbol].split ( ' - ' )[0][:18]
            print ( f"{symbol:<8} {company_name:<20} {analysis['recommendation']:<12} "
                    f"${analysis['current_price']:<9.2f} {analysis['rsi_value']:<6.1f} "
                    f"{analysis['score']:>+3d}" )


def main():
    """
    Main execution function for stock analysis.
    """
    try:
        # Initialize analyzer
        analyzer = StockAnalyzer ()

        # Run complete analysis
        report = analyzer.run_complete_analysis ()

        # Print summary
        analyzer.print_summary ()

    except Exception as e:
        logger.error ( f"Application error: {str ( e )}" )
        raise


if __name__ == "__main__":
    main ()