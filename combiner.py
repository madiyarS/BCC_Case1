import pandas as pd

def combine_csv_files(file1_path, file2_path, output_path='result.csv'):
    """
    Combines two CSV files by merging them on client_code and name columns
    without repeating the common columns.
    
    Args:
        file1_path (str): Path to the first CSV file (client categories)
        file2_path (str): Path to the second CSV file (financial data)
        output_path (str): Path for the output CSV file (default: 'result.csv')
    """
    
    try:
        # Read both CSV files
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        print(f"Loaded {file1_path}: {df1.shape[0]} rows, {df1.shape[1]} columns")
        print(f"Loaded {file2_path}: {df2.shape[0]} rows, {df2.shape[1]} columns")
        
        # Merge the dataframes on client_code and name
        # Using 'inner' join to only include clients that exist in both files
        merged_df = pd.merge(df1, df2, on=['client_code', 'name'], how='inner')
        
        print(f"Merged data: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
        
        # Save to CSV
        merged_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Successfully saved combined data to {output_path}")
        
        # Display first few rows for verification
        print("\nFirst 5 rows of the combined data:")
        print(merged_df.head())
        
        return merged_df
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace these with your actual file paths
    file1 = "top5_categories_analysis.csv"  # Categories file (client_code, name, category_1, category_2, category_3, currency_count, currencies)
    file2 = "Transfers/transfer_summary.csv"  # Financial data file (client_code, name, product, in, out, total)
    
    # Combine the files
    combined_data = combine_csv_files(file1, file2, "result.csv")
    
    if combined_data is not None:
        print(f"\nColumn names in result.csv:")
        print(list(combined_data.columns))