import pandas as pd
import os
import glob
from pathlib import Path

def convert_to_kzt(amount, currency):
    """Convert amount to KZT based on exchange rates"""
    exchange_rates = {
        'EUR': 633,
        'USD': 540,
        'KZT': 1
    }
    return amount * exchange_rates.get(currency, 1)

def process_transfers():
    # Define the folder path
    transfers_folder = 'Transfers'
    
    # Check if Transfers folder exists
    if not os.path.exists(transfers_folder):
        print(f"Error: {transfers_folder} folder not found!")
        return
    
    # Get all CSV files in the Transfers folder
    csv_files = glob.glob(os.path.join(transfers_folder, '*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {transfers_folder} folder!")
        return
    
    print(f"Found {len(csv_files)} CSV files to process...")
    
    # List to store all dataframes
    all_data = []
    
    # Process each CSV file
    for file_path in csv_files:
        try:
            print(f"Processing: {os.path.basename(file_path)}")
            
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Clean column names (remove extra spaces)
            df.columns = df.columns.str.strip()
            
            # Add to combined data
            all_data.append(df)
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue
    
    if not all_data:
        print("No valid data found to process!")
        return
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Convert amounts to KZT
    combined_df['amount_kzt'] = combined_df.apply(
        lambda row: convert_to_kzt(row['amount'], row['currency']), axis=1
    )
    
    # Group by client and calculate aggregations
    summary_data = []
    
    for (client_code, name, product), group in combined_df.groupby(['client_code', 'name', 'product']):
        # Calculate inflows and outflows
        inflows = group[group['direction'] == 'in']['amount_kzt'].sum()
        outflows = group[group['direction'] == 'out']['amount_kzt'].sum()
        total = inflows - outflows
        
        # Count FX transactions
        fx_transactions = group[group['type'].isin(['fx_buy', 'fx_sell'])].shape[0]
        have_fx = 1 if fx_transactions >= 5 else 0
        
        # Count loan payment out transactions
        loan_payment_transactions = group[group['type'] == 'loan_payment_out'].shape[0]
        loan_p_o = 1 if loan_payment_transactions >= 10 else 0
        
        summary_data.append({
            'client_code': int(client_code),
            'name': name,
            'product': product,
            'in': round(inflows, 2),
            'out': round(outflows, 2),
            'total': round(total, 2),
            'have_fx': have_fx,
            'loan_p_o': loan_p_o
        })
    
    # Create summary dataframe
    summary_df = pd.DataFrame(summary_data)
    
    # Sort by client_code for better organization
    summary_df = summary_df.sort_values('client_code')
    
    # Create output filename
    output_file = os.path.join(transfers_folder, 'transfer_summary.csv')
    
    # Save to CSV
    summary_df.to_csv(output_file, index=False)
    
    print(f"\nProcessing completed successfully!")
    print(f"Summary saved to: {output_file}")
    print(f"\nSummary statistics:")
    print(f"Total clients processed: {len(summary_df)}")
    print(f"Total inflows: {summary_df['in'].sum():,.2f} KZT")
    print(f"Total outflows: {summary_df['out'].sum():,.2f} KZT")
    print(f"Net total: {summary_df['total'].sum():,.2f} KZT")
    print(f"Clients with FX activity (≥5 transactions): {summary_df['have_fx'].sum()}")
    print(f"Clients with loan payment activity (≥5 transactions): {summary_df['loan_p_o'].sum()}")
    
    # Display first few rows
    print(f"\nFirst 5 rows of summary:")
    print(summary_df.head().to_string(index=False))

if __name__ == "__main__":
    process_transfers()