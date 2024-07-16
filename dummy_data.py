import json
import random
from faker import Faker
import uuid
from datetime import datetime

faker = Faker()

def generate_customer():
    return {
        "email": faker.email(),
        "customerId": str(uuid.uuid4()),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "profile": {
            "device": faker.word(ext_word_list=['WEB', 'MOBILE', 'UNKNOWN', 'IOS', 'ANDROID', 'MOBILE_WEB']),
            "ipAddress": faker.ipv4(),
            "deviceType": faker.word(ext_word_list=['WEB', 'MOBILE', 'UNKNOWN', 'IOS', 'ANDROID', 'MOBILE_WEB'])
        },
        "account": {
            "accountNumber": faker.iban(),
            "bankCode": faker.bban(),
            "country": faker.country_code()
        }
    }


customers = [generate_customer() for _ in range(100000)]


def pick_random_customer():
    return random.choice(customers)


def generate_transaction():
    from_customer = pick_random_customer()
    to_customer = pick_random_customer()
    while from_customer["customerId"] == to_customer["customerId"]:
        to_customer = pick_random_customer()
    
    transaction_type = random.choice(["WITHDRAWAL", "TRANSFER"])
    
    amount = 0
    rand_num = random.random()
    if rand_num < 0.80:
        amount = random.randint(100, 1000000) 
    elif rand_num < 0.95:
        amount = random.randint(1000000, 5000000)  
    else:
        amount = random.randint(5000000, 10000000) 
    return {
        "fromCustomer": from_customer,
        "toCustomer": to_customer,
        "transaction": {
            "transactionId": str(uuid.uuid4()),
            "amount": amount,
            "date": faker.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S"),
            "description": faker.sentence(),
            "type": transaction_type
        }
    }


transactions = [generate_transaction() for _ in range(5000000)]


with open('transactions.json', 'w') as f:
    json.dump(transactions, f)

print("Data generation complete.")