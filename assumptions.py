import pandas as pd
import numpy as np

def analyze_client_recommendations(input_file='final_result.csv', output_file='assumptions.csv'):
    """
    Analyzes client data and generates product recommendations based on specified rules.
    """
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Initialize results list
    results = []
    
    # Group by client to analyze each client's data
    grouped = df.groupby('client_code')
    
    for client_code, client_data in grouped:
        # Get client name (assuming it's consistent for each client)
        client_name = client_data.iloc[0]['name']
        
        # Get unique values for the client
        avg_monthly_balance = client_data.iloc[0]['avg_monthly_balance_KZT']
        loan_p_o = client_data.iloc[0]['loan_p_o']
        have_fx = client_data.iloc[0]['have_fx']
        currency_count = client_data.iloc[0]['currency_count']
        
        # Initialize recommendations list for this client
        recommendations = []
        
        # Analyze top 5 categories by total amount
        category_totals = {}
        
        # Process categories for each row
        for _, row in client_data.iterrows():
            # Check all category columns (category_1 to category_5)
            for i in range(1, 6):
                cat_col = f'category_{i}'
                if cat_col in row and pd.notna(row[cat_col]):
                    category = row[cat_col]
                    if category not in category_totals:
                        category_totals[category] = 0
                    category_totals[category] += abs(row['total'])
        
        # Sort categories by total amount and get top 5
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_categories = [cat[0] for cat in sorted_categories]
        
        # Rule 1: Check for Travel/Hotel/Taxi categories
        travel_categories = ['Путешествия', 'Отели', 'Такси']
        travel_count = sum(1 for cat in top_5_categories if cat in travel_categories)
        
        if travel_count >= 2:
            recommendations.append('Карта для путешествий')
        
        # Rule 2: Check for Home Entertainment categories
        home_categories = ['Едим дома', 'Смотрим дома', 'Играем дома']
        home_count = sum(1 for cat in top_5_categories if cat in home_categories)
        
        if home_count >= 2:
            recommendations.append('Кредитная карта')
        
        # Rule 3: Check loan_p_o
        if loan_p_o == 1:
            recommendations.append('Кредит наличными')
        
        # Rule 4-6: Check avg_monthly_balance_KZT
        if 400000 < avg_monthly_balance <= 750000:
            recommendations.append('Инвестиции')
            recommendations.append('Депозит сберегательный')
        elif 750000 < avg_monthly_balance <= 1200000:
            recommendations.append('Инвестиции')
            recommendations.append('Депозит накопительный')
        elif avg_monthly_balance > 1200000:
            recommendations.append('Золотые слитки')
        
        # Check for jewelry in categories (additional condition for gold bars)
        jewelry_categories = ['Ювелирные украшения', 'Ювелирные']
        has_jewelry = any(cat in category_totals for cat in jewelry_categories)
        
        if has_jewelry and 'Золотые слитки' not in recommendations:
            recommendations.append('Золотые слитки')
        
        # Rule 7: Check have_fx
        if have_fx == 1:
            recommendations.append('Депозит Мультивалютный')
            recommendations.append('Обмен валют')
        
        # Rule 8: Check currency_count
        if currency_count > 1:
            if 'Депозит Мультивалютный' not in recommendations:
                recommendations.append('Депозит Мультивалютный')
        
        # Check if client qualifies for premium card based on balance or spending
        total_spending = client_data['total'].abs().sum()
        if avg_monthly_balance > 750000 or total_spending > 10000000:
            if 'Премиальная карта' not in recommendations:
                recommendations.append('Премиальная карта')
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for item in recommendations:
            if item not in seen:
                seen.add(item)
                unique_recommendations.append(item)
        
        # Prepare the result
        if unique_recommendations:
            assumption_products = ', '.join(unique_recommendations)
        else:
            assumption_products = 'Стандартные продукты'
        
        # Get the primary product (most used)
        product_counts = client_data['product'].value_counts()
        primary_product = product_counts.index[0] if not product_counts.empty else ''
        
        results.append({
            'client_code': client_code,
            'name': client_name,
            'product': primary_product,
            'assumption_products': assumption_products
        })
    
    # Create DataFrame from results
    result_df = pd.DataFrame(results)
    
    # Sort by client_code
    result_df = result_df.sort_values('client_code')
    
    # Save to CSV
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"Analysis complete! Results saved to {output_file}")
    print(f"Total clients analyzed: {len(results)}")
    
    # Display first few rows as preview
    print("\nPreview of recommendations:")
    print(result_df.head(10).to_string())
    
    # Display statistics
    print("\nRecommendation Statistics:")
    all_recommendations = []
    for r in results:
        if r['assumption_products'] != 'Стандартные продукты':
            all_recommendations.extend(r['assumption_products'].split(', '))
    
    from collections import Counter
    rec_counts = Counter(all_recommendations)
    
    print("\nMost recommended products:")
    for product, count in rec_counts.most_common():
        print(f"  {product}: {count} clients")
    
    return result_df

# Main execution
if __name__ == "__main__":
    # You can customize the file names here
    input_csv = 'final_result.csv'  # Your input file
    output_csv = 'assumptions.csv'  # Output file with recommendations
    
    try:
        # Run the analysis
        recommendations_df = analyze_client_recommendations(input_csv, output_csv)
        
        print("\n✅ Script executed successfully!")
        print(f"📁 Check '{output_csv}' for the complete results.")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_csv}'. Please make sure the file exists in the current directory.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("Please check your CSV file format and ensure all required columns are present.")