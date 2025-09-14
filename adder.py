import pandas as pd
import sys

def merge_csv_files(first_csv_path, second_csv_path, output_path='final_result.csv'):
    """
    Merge two CSV files by adding avg_monthly_balance_KZT column from second CSV to first CSV
    
    Args:
        first_csv_path (str): Path to the first CSV file (base file)
        second_csv_path (str): Path to the second CSV file (source for avg_monthly_balance_KZT)
        output_path (str): Path for the output merged CSV file
    """
    
    try:
        # Read both CSV files
        print(f"Reading {first_csv_path}...")
        df1 = pd.read_csv(first_csv_path)
        
        print(f"Reading {second_csv_path}...")
        df2 = pd.read_csv(second_csv_path)
        
        # Display basic info about the files
        print(f"\nFirst CSV shape: {df1.shape}")
        print(f"First CSV columns: {list(df1.columns)}")
        print(f"\nSecond CSV shape: {df2.shape}")
        print(f"Second CSV columns: {list(df2.columns)}")
        
        # Check if avg_monthly_balance_KZT exists in second file
        if 'avg_monthly_balance_KZT' not in df2.columns:
            print("Error: 'avg_monthly_balance_KZT' column not found in second CSV file")
            return False
        
        # Determine the merge key (assuming it's client_code or the first column)
        # You can modify this logic based on your specific requirements
        merge_key = None
        
        # Check for common columns that could be used as merge key
        common_columns = set(df1.columns) & set(df2.columns)
        
        if 'client_code' in common_columns:
            merge_key = 'client_code'
        elif len(common_columns) > 0:
            merge_key = list(common_columns)[0]
            print(f"Using '{merge_key}' as merge key")
        else:
            print("Error: No common columns found between the two CSV files")
            return False
        
        print(f"Merging on column: '{merge_key}'")
        
        # Create a subset of df2 with only the merge key and avg_monthly_balance_KZT
        df2_subset = df2[[merge_key, 'avg_monthly_balance_KZT']].copy()
        
        # Merge the dataframes
        # Using left join to keep all records from first CSV
        merged_df = pd.merge(df1, df2_subset, on=merge_key, how='left')
        
        # Save the result
        merged_df.to_csv(output_path, index=False)
        print(f"\nMerged CSV saved as: {output_path}")
        print(f"Final shape: {merged_df.shape}")
        print(f"Final columns: {list(merged_df.columns)}")
        
        # Display some statistics
        print(f"\nRecords with avg_monthly_balance_KZT data: {merged_df['avg_monthly_balance_KZT'].notna().sum()}")
        print(f"Records missing avg_monthly_balance_KZT data: {merged_df['avg_monthly_balance_KZT'].isna().sum()}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """
    Main function to run the CSV merger
    """
    
    # You can modify these file paths as needed
    if len(sys.argv) == 3:
        first_csv = sys.argv[1]
        second_csv = sys.argv[2]
    else:
        # Default file names - modify these according to your actual file names
        first_csv = "result.csv"  # Replace with your first CSV file name
        second_csv = "clients.csv"  # Replace with your second CSV file name
    
    print("CSV File Merger")
    print("=" * 50)
    print(f"First CSV (base): {first_csv}")
    print(f"Second CSV (source for avg_monthly_balance_KZT): {second_csv}")
    print(f"Output: result.csv")
    print("=" * 50)
    
    success = merge_csv_files(first_csv, second_csv)
    
    if success:
        print("\n✅ Merge completed successfully!")
    else:
        print("\n❌ Merge failed!")

if __name__ == "__main__":
    main()