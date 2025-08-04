#!/usr/bin/env python3
"""
Example usage of the Stock Market Analyzer tool.

This script demonstrates various ways to use the StockAnalyzer class
for different types of market analysis.
"""

from stock_analyzer import StockAnalyzer
import logging

# Configure logging to see detailed output
logging.basicConfig ( level=logging.INFO )


def basic_analysis_example():
    """
    Example 1: Basic analysis with default stocks
    """
    print ( "=" * 60 )
    print ( "EXAMPLE 1: Basic Analysis with Default Stocks" )
    print ( "=" * 60 )

    # Initialize analyzer with default stocks
    analyzer = StockAnalyzer ()

    # Run complete analysis
    report = analyzer.run_complete_analysis ()

    # Print summary
    analyzer.print_summary ()


def custom_stocks_example():
    """
    Example 2: Analysis with custom stock selection
    """
    print ( "\n" + "=" * 60 )
    print ( "EXAMPLE 2: Custom Stock Selection" )
    print ( "=" * 60 )

    # Define custom stocks for analysis
    tech_stocks = {
        'GOOGL': 'Alphabet Inc. - Technology',
        'META': 'Meta Platforms Inc. - Technology',
        'NFLX': 'Netflix Inc. - Communication Services',
        'ADBE': 'Adobe Inc. - Technology',
        'CRM': 'Salesforce Inc. - Technology',
        'PYPL': 'PayPal Holdings Inc. - Financial Technology'
    }

    # Initialize analyzer with custom stocks
    analyzer = StockAnalyzer ( custom_stocks=tech_stocks )

    # Run analysis with shorter time period
    analyzer.fetch_stock_data ( period='2y' )
    analyzer.clean_and_preprocess_data ()
    analyzer.calculate_technical_indicators ()
    analyzer.analyze_trends ()
    analyzer.create_visualizations ()
    report = analyzer.generate_report ()

    # Print tech sector summary
    print ( "\nTech Sector Analysis Summary:" )
    print ( "-" * 40 )
    analyzer.print_summary ()


def step_by_step_example():
    """
    Example 3: Step-by-step analysis with custom configuration
    """
    print ( "\n" + "=" * 60 )
    print ( "EXAMPLE 3: Step-by-Step Custom Analysis" )
    print ( "=" * 60 )

    # Define dividend-focused stocks
    dividend_stocks = {
        'KO': 'The Coca-Cola Company - Consumer Staples',
        'PEP': 'PepsiCo Inc. - Consumer Staples',
        'JNJ': 'Johnson & Johnson - Healthcare',
        'PG': 'Procter & Gamble Co. - Consumer Staples',
        'VZ': 'Verizon Communications Inc. - Telecommunications',
        'T': 'AT&T Inc. - Telecommunications'
    }

    analyzer = StockAnalyzer ( custom_stocks=dividend_stocks )

    # Step 1: Fetch data
    print ( "Step 1: Fetching stock data..." )
    success = analyzer.fetch_stock_data ( period='3y' )
    if not success:
        print ( "Failed to fetch data. Exiting." )
        return

    # Step 2: Clean data
    print ( "Step 2: Cleaning and preprocessing data..." )
    analyzer.clean_and_preprocess_data ()

    # Step 3: Calculate indicators
    print ( "Step 3: Calculating technical indicators..." )
    analyzer.calculate_technical_indicators ()

    # Step 4: Analyze trends
    print ( "Step 4: Performing trend analysis..." )
    analyzer.analyze_trends ()

    # Step 5: Create visualizations (optional)
    print ( "Step 5: Generating visualizations..." )
    analyzer.create_visualizations ()

    # Step 6: Generate report
    print ( "Step 6: Creating analysis report..." )
    report = analyzer.generate_report ()

    # Display results
    print ( "\nDividend Stocks Analysis:" )
    print ( "-" * 40 )

    # Show detailed analysis for each stock
    for symbol, analysis in analyzer.analysis_results.items ():
        print ( f"\n{symbol} - {analyzer.stocks[symbol]}" )
        print ( f"  Current Price: ${analysis['current_price']:.2f}" )
        print ( f"  Recommendation: {analysis['recommendation']}" )
        print ( f"  RSI: {analysis['rsi_value']:.1f} ({analysis['rsi_signal']})" )
        print ( f"  Volatility: {analysis['volatility']:.2f}" )


def sector_analysis_example():
    """
    Example 4: Multi-sector analysis
    """
    print ( "\n" + "=" * 60 )
    print ( "EXAMPLE 4: Multi-Sector Analysis" )
    print ( "=" * 60 )

    # Define stocks from various sectors
    diversified_portfolio = {
        # Technology
        'AAPL': 'Apple Inc. - Technology',
        'MSFT': 'Microsoft Corporation - Technology',

        # Healthcare
        'UNH': 'UnitedHealth Group Inc. - Healthcare',
        'PFE': 'Pfizer Inc. - Healthcare',

        # Financial
        'JPM': 'JPMorgan Chase & Co. - Financial',
        'BAC': 'Bank of America Corp. - Financial',

        # Consumer Discretionary
        'AMZN': 'Amazon.com Inc. - Consumer Discretionary',
        'HD': 'The Home Depot Inc. - Consumer Discretionary',

        # Energy
        'XOM': 'Exxon Mobil Corporation - Energy',
        'CVX': 'Chevron Corporation - Energy'
    }

    analyzer = StockAnalyzer ( custom_stocks=diversified_portfolio )
    report = analyzer.run_complete_analysis ()

    # Analyze by sector
    sectors = {}
    for symbol, description in diversified_portfolio.items ():
        sector = description.split ( ' - ' )[1]
        if sector not in sectors:
            sectors[sector] = []
        sectors[sector].append ( symbol )

    print ( "\nSector Performance Summary:" )
    print ( "-" * 50 )

    for sector, symbols in sectors.items ():
        print ( f"\n{sector.upper ()} SECTOR:" )
        sector_scores = []

        for symbol in symbols:
            if symbol in analyzer.analysis_results:
                analysis = analyzer.analysis_results[symbol]
                score = analysis['score']
                recommendation = analysis['recommendation']
                price = analysis['current_price']

                print ( f"  {symbol}: {recommendation} (Score: {score:+d}, Price: ${price:.2f})" )
                sector_scores.append ( score )

        if sector_scores:
            avg_score = sum ( sector_scores ) / len ( sector_scores )
            print ( f"  → Sector Average Score: {avg_score:.1f}" )


def quick_screening_example():
    """
    Example 5: Quick screening for buy/sell opportunities
    """
    print ( "\n" + "=" * 60 )
    print ( "EXAMPLE 5: Quick Stock Screening" )
    print ( "=" * 60 )

    # Large cap stocks for screening
    large_caps = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'AMZN': 'Amazon.com Inc.',
        'TSLA': 'Tesla Inc.',
        'META': 'Meta Platforms Inc.',
        'NVDA': 'NVIDIA Corporation',
        'BRK-B': 'Berkshire Hathaway Inc.',
        'V': 'Visa Inc.',
        'JNJ': 'Johnson & Johnson'
    }

    analyzer = StockAnalyzer ( custom_stocks=large_caps )

    # Quick analysis
    analyzer.fetch_stock_data ( period='1y' )  # Use 1 year for faster processing
    analyzer.clean_and_preprocess_data ()
    analyzer.calculate_technical_indicators ()
    analyzer.analyze_trends ()

    # Screen for opportunities
    buy_candidates = []
    sell_candidates = []

    for symbol, analysis in analyzer.analysis_results.items ():
        if "Buy" in analysis['recommendation']:
            buy_candidates.append ( (symbol, analysis) )
        elif "Sell" in analysis['recommendation']:
            sell_candidates.append ( (symbol, analysis) )

    # Display screening results
    print ( f"\nBUY CANDIDATES ({len ( buy_candidates )} found):" )
    print ( "-" * 40 )
    for symbol, analysis in sorted ( buy_candidates, key=lambda x: x[1]['score'], reverse=True ):
        print ( f"{symbol}: {analysis['recommendation']} (Score: {analysis['score']:+d}, "
                f"RSI: {analysis['rsi_value']:.1f}, Price: ${analysis['current_price']:.2f})" )

    print ( f"\nSELL CANDIDATES ({len ( sell_candidates )} found):" )
    print ( "-" * 40 )
    for symbol, analysis in sorted ( sell_candidates, key=lambda x: x[1]['score'] ):
        print ( f"{symbol}: {analysis['recommendation']} (Score: {analysis['score']:+d}, "
                f"RSI: {analysis['rsi_value']:.1f}, Price: ${analysis['current_price']:.2f})" )


def main():
    """
    Run all examples to demonstrate the tool's capabilities.
    """
    print ( "Stock Market Analyzer - Usage Examples" )
    print ( "=" * 80 )
    print ( "This script demonstrates various ways to use the analyzer." )
    print ( "Each example shows different features and use cases." )
    print ( "=" * 80 )

    try:
        # Run all examples
        basic_analysis_example ()
        custom_stocks_example ()
        step_by_step_example ()
        sector_analysis_example ()
        quick_screening_example ()

        print ( "\n" + "=" * 80 )
        print ( "ALL EXAMPLES COMPLETED SUCCESSFULLY!" )
        print ( "Check the generated files for detailed analysis results." )
        print ( "=" * 80 )

    except Exception as e:
        print ( f"Error running examples: {str ( e )}" )
        print ( "Please check your internet connection and try again." )


if __name__ == "__main__":
    main ()