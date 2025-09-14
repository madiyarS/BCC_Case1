import pandas as pd
import random
from datetime import datetime

def load_data(filename='assumptions.csv'):
    """Load CSV file with proper encoding"""
    try:
        # Try UTF-8 first
        df = pd.read_csv(filename, encoding='utf-8')
    except:
        try:
            # Try Windows-1251 (common for Russian text)
            df = pd.read_csv(filename, encoding='windows-1251')
        except:
            # Try Latin-1 as fallback
            df = pd.read_csv(filename, encoding='latin-1')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Clean string columns
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    
    return df

def parse_assumption_products(assumption_str):
    """Parse the assumption_products string into a list"""
    if pd.isna(assumption_str):
        return []
    # Split by comma and clean up
    products = [p.strip() for p in str(assumption_str).split(',')]
    return products

def get_alternative_product(current_product, assumption_products):
    """Get an alternative product from the assumption list"""
    # Parse assumption products
    available_products = parse_assumption_products(assumption_products)
    
    # Remove current product from alternatives
    alternatives = [p for p in available_products if p != current_product]
    
    # If no alternatives, offer "Кредит наличными"
    if not alternatives:
        return "Кредит наличными"
    
    # Return the first alternative (or random choice)
    return alternatives[0]

def generate_message(name, product_type):
    """Generate personalized message based on product type"""
    
    # Dictionary of product types and their corresponding messages
    messages = {
        "Карта для путешествий": f"{name}, у вас активные траты на поездки и такси. С картой для путешествий часть расходов вернётся кешбэком. Оформить карту",
        
        "Премиальная карта": f"{name}, у вас стабильный остаток и траты в премиум-сегменте. Премиальная карта даст повышенный кешбэк и привилегии. Оформить сейчас",
        
        "Кредитная карта": f"{name}, ваши активные категории — покупки и онлайн-сервисы. Кредитная карта даёт до 10% кешбэка. Оформить карту",
        
        "Золотые слитки": f"{name}, у вас есть свободные средства. Золотые слитки — надёжный способ сохранить капитал. Узнать подробнее",
        
        "Депозит Мультивалютный": f"{name}, вы работаете с валютой. Мультивалютный депозит поможет выгодно разместить средства. Открыть депозит",
        
        "Обмен валют": f"{name}, вы часто конвертируете валюту. В приложении доступен выгодный курс обмена. Настроить обмен",
        
        "Инвестиции": f"{name}, попробуйте инвестиции с низким порогом входа и без комиссий на старт. Открыть счёт",
        
        "Кредит наличными": f"{name}, если нужны средства на важные цели — доступен кредит с удобными выплатами. Узнать лимит",
        
        "Депозит накопительный": f"{name}, у вас остаются свободные средства. Накопительный депозит поможет копить с выгодой. Открыть вклад"
    }
    
    # Default message if product type not found
    default_message = f"{name}, у нас есть выгодное предложение специально для вас. Узнать подробнее"
    
    # Find matching message
    for key, message in messages.items():
        if key.lower() in product_type.lower():
            return message
    
    # If no exact match, try partial matches
    if "карта" in product_type.lower() and "кредит" in product_type.lower():
        return messages["Кредитная карта"]
    elif "премиальная" in product_type.lower():
        return messages["Премиальная карта"]
    elif "путешеств" in product_type.lower():
        return messages["Карта для путешествий"]
    elif "золот" in product_type.lower():
        return messages["Золотые слитки"]
    elif "депозит" in product_type.lower() or "вклад" in product_type.lower():
        if "мультивалют" in product_type.lower():
            return messages["Депозит Мультивалютный"]
        else:
            return messages["Депозит накопительный"]
    elif "обмен" in product_type.lower() and "валют" in product_type.lower():
        return messages["Обмен валют"]
    elif "инвестиц" in product_type.lower():
        return messages["Инвестиции"]
    elif "наличн" in product_type.lower():
        return messages["Кредит наличными"]
    
    return default_message

def process_assumptions(input_file='assumptions.csv', output_file='recommendations.csv'):
    """Main function to process assumptions and generate recommendations"""
    
    print("Loading data...")
    df = load_data(input_file)
    
    print(f"Loaded {len(df)} records")
    print(f"Columns: {df.columns.tolist()}")
    
    # Prepare output data
    results = []
    
    for index, row in df.iterrows():
        client_code = row['client_code']
        name = row['name']
        current_product = row['product']
        assumption_products = row['assumption_products']
        
        # Get alternative product
        recommended_product = get_alternative_product(current_product, assumption_products)
        
        # Generate message
        message = generate_message(name, recommended_product)
        
        # Add to results
        results.append({
            'client_code': client_code,
            'name': name,
            'assumption_message': message
        })
        
        print(f"Processed client {client_code}: {name} -> {recommended_product}")
    
    # Create output DataFrame
    output_df = pd.DataFrame(results)
    
    # Save to CSV
    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nResults saved to {output_file}")
    
    # Display first few results
    print("\nFirst 5 recommendations:")
    print(output_df.head().to_string())
    
    return output_df

def main():
    """Main execution function"""
    try:
        # Process the assumptions
        results = process_assumptions()
        
        print(f"\n✅ Successfully processed {len(results)} clients")
        print(f"Output file: recommendations.csv")
        
        # Show statistics
        print("\nStatistics:")
        print(f"Total clients: {len(results)}")
        print(f"Average message length: {results['assumption_message'].str.len().mean():.0f} characters")
        
    except FileNotFoundError:
        print("❌ Error: assumptions.csv file not found!")
        print("Please make sure the file is in the same directory as this script.")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("Please check your CSV file format.")

if __name__ == "__main__":
    main()