import pandas as pd
import os
import glob
from collections import defaultdict

def analyze_transaction_categories(folder_path, excluded_categories=None, output_file='top5_categories_analysis.csv'):
    """
    Analyze transaction data to find top 5 spending categories for each person.
    
    Args:
        folder_path (str): Path to folder containing CSV files
        excluded_categories (list): List of categories to exclude from analysis
        output_file (str): Name of output CSV file
    """
    
    if excluded_categories is None:
        excluded_categories = ['Продукты питания', 'Кафе и рестораны']
    
    # Find all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(f"  - {os.path.basename(file)}")
    
    # Read and combine all CSV files
    all_transactions = []
    
    for file in csv_files:
        try:
            # Read CSV with flexible encoding handling
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='cp1251')  # Common for Russian text
            except:
                df = pd.read_csv(file, encoding='latin-1')
            
            print(f"Loaded {len(df)} transactions from {os.path.basename(file)}")
            all_transactions.append(df)
            
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
            continue
    
    if not all_transactions:
        print("No valid transaction data found!")
        return
    
    # Combine all dataframes
    combined_df = pd.concat(all_transactions, ignore_index=True)
    
    # Clean column names (remove extra spaces)
    combined_df.columns = combined_df.columns.str.strip()
    
    print(f"\nTotal transactions loaded: {len(combined_df)}")
    print(f"Columns found: {list(combined_df.columns)}")
    
    # Ensure required columns exist
    required_columns = ['client_code', 'name', 'category', 'amount', 'currency']
    missing_columns = [col for col in required_columns if col not in combined_df.columns]
    
    if missing_columns:
        print(f"Warning: Missing columns: {missing_columns}")
        print("Available columns:", list(combined_df.columns))
        return
    
    # Clean and prepare data
    combined_df['amount'] = pd.to_numeric(combined_df['amount'], errors='coerce')
    combined_df = combined_df.dropna(subset=['amount'])
    
    # Remove excluded categories
    print(f"\nExcluding categories: {excluded_categories}")
    filtered_df = combined_df[~combined_df['category'].isin(excluded_categories)].copy()
    
    print(f"Transactions after filtering: {len(filtered_df)}")
    
    # Group by person and analyze spending by category
    results = []
    people_with_no_categories = []
    
    # Group by client_code and name (from original data to get currencies)
    all_person_groups = combined_df.groupby(['client_code', 'name'])
    
    for (client_code, name), person_data in all_person_groups:
        # Get unique currencies for this person (from all transactions)
        currencies = person_data['currency'].unique()
        currency_count = len(currencies)
        currencies_str = ', '.join(sorted(currencies))
        
        # Get filtered data for this person (excluding categories)
        person_filtered = filtered_df[
            (filtered_df['client_code'] == client_code) & 
            (filtered_df['name'] == name)
        ]
        
        if len(person_filtered) == 0:
            # This person only has excluded categories
            people_with_no_categories.append(name)
            result = {
                'client_code': client_code,
                'name': name,
                'category_1': '',
                'category_2': '',
                'category_3': '',
                'category_4': '',
                'category_5': '',
                'currency_count': currency_count,
                'currencies': currencies_str
            }
        else:
            # Group by category and sum amounts
            category_spending = person_filtered.groupby('category')['amount'].sum().sort_values(ascending=False)
            
            # Get top 5 categories
            top_categories = category_spending.head(5)
            
            # Create result row
            result = {
                'client_code': client_code,
                'name': name,
                'category_1': top_categories.index[0] if len(top_categories) > 0 else '',
                'category_2': top_categories.index[1] if len(top_categories) > 1 else '',
                'category_3': top_categories.index[2] if len(top_categories) > 2 else '',
                'category_4': top_categories.index[3] if len(top_categories) > 3 else '',
                'category_5': top_categories.index[4] if len(top_categories) > 4 else '',
                'currency_count': currency_count,
                'currencies': currencies_str
            }
        
        results.append(result)

    # Create results dataframe
    results_df = pd.DataFrame(results)
    
    # Sort by client_code and name for consistent output
    results_df = results_df.sort_values(['client_code', 'name'])
    
    # Save to CSV
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nAnalysis complete!")
    print(f"Found {len(results_df)} unique people")
    print(f"Results saved to: {output_file}")
    print(f"Columns: client_code, name, category_1, category_2, category_3, category_4, category_5, currency_count, currencies")
    
    # Display summary
    print(f"\nSummary:")
    print(f"- Total people analyzed: {len(results_df)}")
    print(f"- People with non-excluded categories: {len(results_df) - len(people_with_no_categories)}")
    print(f"- People with only excluded categories: {len(people_with_no_categories)}")
    print(f"- Categories excluded: {len(excluded_categories)}")
    
    if people_with_no_categories:
        print(f"\nPeople with only excluded categories ({len(people_with_no_categories)}):")
        for name in people_with_no_categories[:10]:  # Show first 10
            print(f"  - {name}")
        if len(people_with_no_categories) > 10:
            print(f"  ... and {len(people_with_no_categories) - 10} more")
    
    # Show sample of results
    print(f"\nFirst 5 results with top 5 categories each:")
    print(results_df.head().to_string(index=False))
    
    return results_df

def analyze_category_coverage(folder_path, excluded_categories=None):
    """
    Analyze how many people would have empty results if we exclude certain categories.
    This helps you decide which categories to exclude.
    """
    if excluded_categories is None:
        excluded_categories = ['Продукты питания', 'Кафе и рестораны']
    
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return
    
    all_transactions = []
    
    for file in csv_files:
        try:
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='cp1251')
            except:
                df = pd.read_csv(file, encoding='latin-1')
            
            all_transactions.append(df)
            
        except Exception as e:
            continue
    
    if not all_transactions:
        return
    
    combined_df = pd.concat(all_transactions, ignore_index=True)
    combined_df.columns = combined_df.columns.str.strip()
    
    # Get all unique people
    all_people = combined_df.groupby(['client_code', 'name']).size().reset_index(name='transaction_count')
    total_people = len(all_people)
    
    # Filter out excluded categories
    filtered_df = combined_df[~combined_df['category'].isin(excluded_categories)]
    
    # Get people who still have categories after filtering
    people_with_categories = filtered_df.groupby(['client_code', 'name']).size().reset_index(name='transaction_count')
    people_with_data = len(people_with_categories)
    
    print(f"\nCategory Coverage Analysis:")
    print(f"Total people: {total_people}")
    print(f"People with non-excluded categories: {people_with_data}")
    print(f"People with only excluded categories: {total_people - people_with_data}")
    print(f"Coverage: {(people_with_data/total_people)*100:.1f}%")
    
    # Show category distribution
    print(f"\nCategory frequency (all transactions):")
    category_counts = combined_df['category'].value_counts()
    print(category_counts.head(10).to_string())
    
    return {
        'total_people': total_people,
        'people_with_data': people_with_data,
        'coverage_percent': (people_with_data/total_people)*100
    }

# Example usage
if __name__ == "__main__":
    # Set your folder path here
    folder_path = "Transactions"  # Change this to your actual folder path
    
    # You can customize excluded categories
    excluded_categories = ['Продукты питания', 'Кафе и рестораны']
    
    # First, let's see what categories exist in your data
    print("=== Category Coverage Analysis ===")
    analyze_category_coverage(folder_path, excluded_categories)
    
    print("\n" + "="*50)
    print("=== Running Top 5 Categories Analysis ===")
    
    # Run the analysis
    try:
        results = analyze_transaction_categories(
            folder_path=folder_path,
            excluded_categories=excluded_categories,
            output_file='top5_categories_analysis.csv'
        )
        
        if results is not None:
            print(f"\n✅ Analysis completed successfully!")
            print(f"📁 Output file: top5_categories_analysis.csv")
            print(f"👥 Analyzed {len(results)} people")
            print(f"🔝 Shows top 5 spending categories for each person")
            
    except FileNotFoundError:
        print(f"❌ Folder '{folder_path}' not found!")
        print("Please update the 'folder_path' variable with the correct path to your Transactions folder.")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("Please check your CSV files and folder path.")