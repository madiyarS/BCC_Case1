# Personalized Push Notification System for Bank Clients

## 📋 Overview

This project addresses the problem of generic, irrelevant push notifications that banks send to all clients. Instead of sending the same message like "Open this card" to everyone, our solution analyzes individual client behavior over 3 months and generates personalized recommendations with tailored push notifications.

**Problem**: Low engagement and conversion rates due to irrelevant notifications, leading to notification fatigue and missed opportunities for both clients (cashback, interest, fee savings) and banks (sales, loyalty).

**Solution**: A data-driven system that analyzes client behavior, calculates expected benefits for each product, selects the most beneficial product, and generates personalized push notifications with proper tone of voice.

## 🎯 Project Goals

1. **Analyze** fictional client behavior using 3 months of transaction data
2. **Calculate** expected benefits for each client across different banking products
3. **Select** the most beneficial product for each individual client
4. **Generate** personalized push notifications following brand tone of voice guidelines

**Output**: CSV file with `client_code,product,push_notification`

## 📊 Dataset Structure

### Input Data Sources (60 clients total)

#### Client Profiles
- `client_code`, `name`, `status`, `age`, `city`, `avg_monthly_balance_KZT`
- **Client Statuses**: Студент / Зарплатный клиент / Премиальный клиент / Стандартный клиент

#### Transactions (3 months per client)
- `date`, `category`, `amount`, `currency`, `client_code`
- **Categories**: Одежда и обувь, Продукты питания, Кафе и рестораны, Медицина, Авто, Спорт, Развлечения, АЗС, Кино, Питомцы, Книги, Цветы, Едим дома, Смотрим дома, Играем дома, Косметика и Парфюмерия, Подарки, Ремонт дома, Мебель, Спа и массаж, Ювелирные украшения, Такси, Отели, Путешествия

#### Transfers (3 months per client)
- `date`, `type`, `direction` (in|out), `amount`, `currency`, `client_code`
- **Transfer Types**: salary_in, stipend_in, family_in, cashback_in, refund_in, card_in, p2p_out, card_out, atm_withdrawal, utilities_out, loan_payment_out, cc_repayment_out, installment_payment_out, fx_buy, fx_sell, invest_out, invest_in, deposit_topup_out, deposit_fx_topup_out, deposit_fx_withdraw_in, gold_buy_out, gold_sell_in

## 🏦 Product Catalog & Benefit Signals

### 1. Карта для путешествий (Travel Card)
- **Benefits**: Enhanced cashback/privileges for Travel, Taxi, transport
- **Signals**: Spending on Travel/Hotels/Taxi, USD/EUR transactions, business trips
- **Metric**: `benefit = 4% * spend(Travel + Taxi + transport tickets)`

### 2. Премиальная карта (Premium Card)
- **Benefits**: 2-4% base cashback, enhanced cashback on Jewelry/Cosmetics/Restaurants, free withdrawals/transfers
- **Signals**: High avg_monthly_balance_KZT/deposits, frequent ATM withdrawals and transfers, active restaurant/cosmetics/jewelry spending
- **Metric**: `benefit = tier_cashback * base_spend + 4% * spend(jewelry+cosmetics+restaurants) + saved_fees`

### 3. Кредитная карта (Credit Card)
- **Benefits**: Up to 10% in 3 favorite categories (monthly selection) + 10% on online services, grace period up to 2 months, installments 3-24 months
- **Signals**: Clear top spending categories, many online services, installment payments present

### 4. Обмен валют (Currency Exchange)
- **Benefits**: Spread savings, auto-purchase at target rate
- **Signals**: fx_buy/fx_sell activities, regular USD/EUR spending

### 5. Кредит наличными (Cash Loan)
- **Benefits**: Quick access to financing, flexible repayments
- **Signals**: Cash flow gaps (outflows ≫ inflows), low balance, regular loan payments

### 6. Депозит мультивалютный (Multi-currency Deposit)
- **Benefits**: Interest + convenient currency storage, flexible deposits/withdrawals
- **Signals**: Free balance + FX activity + foreign spending

### 7. Депозит сберегательный (Savings Deposit)
- **Benefits**: Maximum rate due to no deposits/withdrawals
- **Signals**: Stable large balance, low expense volatility

### 8. Депозит накопительный (Accumulation Deposit)
- **Benefits**: Enhanced rate, deposits "yes", withdrawals "no"
- **Signals**: Regular small balances + periodic deposits

### 9. Инвестиции (Investment Account)
- **Benefits**: Zero/reduced commissions, low entry threshold
- **Signals**: Free money, growth interest (no return promises)

### 10. Золотые слитки (Gold Bars)
- **Benefits**: Protective asset/diversification
- **Signals**: High liquidity, interest in precious metals/value preservation

## 📱 Push Notification Guidelines

### Message Structure
1. **Personal context** (observation about spending/behavior)
2. **Benefit explanation** (how the product solves the problem)
3. **Clear CTA** (2-4 words)

### Tone of Voice
- Equal, simple, and human; friendly
- Address with "вы" (lowercase), no dramatization or moralizing
- Important information first, no fluff/bureaucracy/passive voice
- Light, unobtrusive humor allowed; 0-1 emoji if meaningful
- For youth: less formal, more lively; no direct slang

### Editorial Policy & Format
- No CAPS; maximum one exclamation mark (only when appropriate)
- Length for channel (target 180-220 characters for push)
- Date: dd.mm.yyyy or "30 августа 2025" where appropriate
- Numbers: decimal comma; thousand separators with spaces
- Currency: consistent format (interface - symbol; SMS - "тг"); separate amount and currency with space (2 490 ₸)
- Links/buttons: action verbs - "Открыть", "Настроить", "Посмотреть"
- No "loud" promises/pressure; don't abuse scarcity triggers

## 📈 Evaluation Metrics (Max 40 points)

### 1. Product Accuracy (up to 20 points)
Position of "reference" best product in your Top-4:
- Exact match → 20 points
- 2nd best → 15 points
- 3rd best → 10 points
- 4th best → 5 points
- Not in Top-4 → 0 points

### 2. Push Quality (up to 20 points)
4 criteria × 5 points each:
- **Personalization and relevance**
- **TOV compliance**
- **Clarity and brevity** (1 thought, 1 CTA)
- **Editorial policy and format**

**Final Score**: Average across 60 clients (each up to 40 points)

## 📋 Output Format

```csv
client_code,product,push_notification
1,Карта для путешествий,"Рамазан, в августе вы сделали 12 поездок на такси на 27 400 ₸. С картой для путешествий вернули бы ≈1 100 ₸. Откройте карту в приложении."
2,Премиальная карта,"Алия, у вас высокий остаток на счету это дает вам большие возможности. Премиальная карта даст до 4% кешбэка на все покупки и бесплатные снятия. Подключите сейчас."
```

## 🚀 Getting Started

1. **Data Preparation**: Ensure you have client profiles, transactions, and transfers data in the specified format
2. **Analysis**: Run behavioral analysis to identify spending patterns and product signals
3. **Benefit Calculation**: Calculate expected benefits for each product per client
4. **Product Selection**: Choose the most beneficial product for each client
5. **Notification Generation**: Create personalized push notifications following TOV guidelines
6. **Output**: Generate final CSV file with recommendations



## 🛠️ Technologies Used

- Python 3.8+
- Pandas for data manipulation
- NumPy for numerical calculations
- CSV for data I/O

## 📞 Contact

For questions or clarifications about this project, please refer to the original case study documentation or contact the development team.

---

*This solution aims to transform generic banking communications into personalized, value-driven interactions that benefit both clients and the bank through improved engagement and conversion rates.*
