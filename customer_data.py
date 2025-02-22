import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

class StarbucksDataGenerator:
    def __init__(self, seed=42):
        self.fake = Faker()
        np.random.seed(seed)
        random.seed(seed)
        
        self.drink_types = ['Latte', 'Cappuccino', 'Americano', 'Espresso', 'Frappuccino', 
                           'Cold Brew', 'Mocha', 'Tea', 'Hot Chocolate']
        self.food_items = ['Croissant', 'Muffin', 'Sandwich', 'Cake Pop', 'Cookie', 
                          'Bagel', 'Protein Box', 'Oatmeal']
        self.locations = ['Mall', 'Street Corner', 'Airport', 'Drive-thru', 'University Campus']
        self.store_types = ['High Traffic', 'Suburban', 'Urban Core', 'Travel', 'University']
        
    def generate_customer_demographics(self, n_customers=500):
        occupations = ['Student', 'Professional', 'Manager', 'Teacher', 'Healthcare', 
                      'Technology', 'Sales', 'Retired', 'Other']
        education_levels = ['High School', 'Some College', 'Bachelor', 'Master', 'PhD']
        
        data = {
            'customer_id': range(1, n_customers + 1),
            'age': np.random.randint(18, 75, n_customers),
            'income': np.random.normal(60000, 20000, n_customers),
            'occupation': [random.choice(occupations) for _ in range(n_customers)],
            'education': [random.choice(education_levels) for _ in range(n_customers)],
            'family_size': np.random.randint(1, 6, n_customers),
            'location_type': [random.choice(['Urban', 'Suburban', 'Rural']) for _ in range(n_customers)]
        }
        
        return pd.DataFrame(data)
    
    def generate_store_data(self, n_stores=5):
        data = {
            'store_id': range(1, n_stores + 1),
            'location_type': [random.choice(self.locations) for _ in range(n_stores)],
            'store_type': [random.choice(self.store_types) for _ in range(n_stores)],
            'avg_daily_traffic': np.random.randint(200, 1000, n_stores),
            'competition_nearby': np.random.randint(0, 5, n_stores),
            'opening_year': np.random.randint(2010, 2024, n_stores),
            'sq_footage': np.random.randint(1000, 3000, n_stores)
        }
        
        return pd.DataFrame(data)
    
    def generate_purchase_history(self, customer_ids, store_ids, n_transactions=2500):
        # Generate random dates within the last year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        dates = [self.fake.date_time_between(start_date=start_date, end_date=end_date) 
                for _ in range(n_transactions)]
        
        data = {
            'transaction_id': range(1, n_transactions + 1),
            'customer_id': np.random.choice(customer_ids, n_transactions),
            'store_id': np.random.choice(store_ids, n_transactions),
            'date': dates,
            'time': [d.time() for d in dates],
            'drink_type': [random.choice(self.drink_types) for _ in range(n_transactions)],
            'food_item': [random.choice(['None'] + self.food_items) for _ in range(n_transactions)],
            'drink_price': np.random.uniform(3.5, 6.5, n_transactions),
            'food_price': np.random.uniform(0, 8, n_transactions),
            'payment_method': np.random.choice(['Mobile', 'Card', 'Cash'], n_transactions, 
                                             p=[0.6, 0.3, 0.1]),
            'order_method': np.random.choice(['Mobile App', 'In-Store'], n_transactions, 
                                           p=[0.4, 0.6])
        }
        
        # Calculate total amount
        df = pd.DataFrame(data)
        df['total_amount'] = df['drink_price'] + df['food_price']
        return df
    
    def generate_loyalty_data(self, customer_ids):
        n_customers = len(customer_ids)
        join_dates = [self.fake.date_between(start_date='-2y') for _ in range(n_customers)]
        
        data = {
            'customer_id': customer_ids,
            'join_date': join_dates,
            'membership_tier': np.random.choice(['Green', 'Gold'], n_customers, p=[0.7, 0.3]),
            'total_points': np.random.randint(0, 1000, n_customers),
            'points_redeemed': np.random.randint(0, 500, n_customers),
            'promotional_offers_used': np.random.randint(0, 10, n_customers),
            'mobile_app_user': np.random.choice([True, False], n_customers, p=[0.8, 0.2])
        }
        
        return pd.DataFrame(data)

def main():
    # Initialize generator
    generator = StarbucksDataGenerator()
    
    # Generate datasets
    demographics = generator.generate_customer_demographics(n_customers=500)
    stores = generator.generate_store_data(n_stores=5)
    purchases = generator.generate_purchase_history(
        demographics['customer_id'], 
        stores['store_id'], 
        n_transactions=2500  # Reduced proportionally
    )
    loyalty = generator.generate_loyalty_data(demographics['customer_id'])
    
    # Save to CSV files
    demographics.to_csv('customer_demographics.csv', index=False)
    stores.to_csv('store_data.csv', index=False)
    purchases.to_csv('purchase_history.csv', index=False)
    loyalty.to_csv('loyalty_data.csv', index=False)
    
if __name__ == "__main__":
    main()
