import json
import random
import time
import csv

from faker import Faker
import uuid
import requests
from datetime import datetime

faker = Faker()

Username = "ifedamilola2009@gmail.com"
Password = "123@ifeDAM567"
BaseUrl = "https://test.usekudi.com/api/"

header = [
    'debitCustomer_email', 'debitCustomer_customerId', 'debitCustomer_name', 'debitCustomer_phone',
    'debitCustomer_DeviceId', 'debitCustomer_ipAddress', 'debitCustomer_deviceType',
    'debitCustomer_accountNumber', 'debitCustomer_bankCode', 'debitCustomer_country',
    'creditCustomer_email', 'creditCustomer_customerId', 'creditCustomer_name', 'creditCustomer_phone',
    'creditCustomer_accountNumber', 'creditCustomer_bankCode', 'creditCustomer_country',
    'transaction_transactionId', 'transaction_amount', 'transaction_TransactionDate',
    'transaction_description', 'transaction_type', 'ObservatoryId'
]
rows = []


def login():
    h = {
        "Content-Type": "application/json"
    }

    record = dict()
    record["Username"] = Username
    record["Password"] = Password
    response = requests.post(BaseUrl + "auth/login", data=json.dumps(record), headers=h)
    if response.status_code == 200:
        result = response.json()
        return result['data']['token']


Token = str(login())
headers = {
    "Authorization": "Bearer " + Token,
    "Content-Type": "application/json"
}


def generate_row(data):
    # Extracting relevant fields
    row = [

        data['debitCustomer']['email'],
        data['debitCustomer']['customerId'],
        data['debitCustomer']['name'],
        data['debitCustomer']['phone'],
        data['debitCustomer']['Device']['DeviceId'],
        data['debitCustomer']['Device']['ipAddress'],
        data['debitCustomer']['Device']['deviceType'],
        data['debitCustomer']['account']['accountNumber'],
        data['debitCustomer']['account']['bankCode'],
        data['debitCustomer']['account']['country'],

        data['creditCustomer']['email'],
        data['creditCustomer']['customerId'],
        data['creditCustomer']['name'],
        data['creditCustomer']['phone'],
        data['creditCustomer']['account']['accountNumber'],
        data['creditCustomer']['account']['bankCode'],
        data['creditCustomer']['account']['country'],

        data['transaction']['transactionId'],
        data['transaction']['amount'],
        data['transaction']['TransactionDate'],
        data['transaction']['description'],
        data['transaction']['type'],
        data['ObservatoryId']
    ]
    # Define the header for the CSV
    rows.append(row)

def generate_csv(rows):
    with open('transaction_data5.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header
        writer.writerows(rows)  # Write the rows

def get_banks():
    response = requests.get(BaseUrl + "bank/all", headers=headers)
    if response.status_code == 200:
        return response.json()['data']


banks = get_banks()


def generate_customer():
    bank = random.choice(banks)
    return {
        "email": faker.email(),
        "customerId": str(uuid.uuid4()),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "Device": {
            "DeviceId": faker.uuid4(),
            "ipAddress": faker.ipv4(),
            "deviceType": random.randint(0, 5)
        },
        "account": {
            "accountNumber": faker.iban(),
            "bankCode": bank['code'],
            "country": "NGN"
        }
    }


def pick_random_customer():
    return random.choice(customers)


def post(t):
    data = t
    response = requests.post(BaseUrl + "transfer/IngestAndQueue",
                             headers=headers, json=t)
    return response


def generate_transaction():
    from_customer = pick_random_customer()
    to_customer = pick_random_customer()
    while from_customer["customerId"] == to_customer["customerId"]:
        to_customer = pick_random_customer()

    transaction_type = 1

    amount = 0
    rand_num = random.random()
    if rand_num < 0.80:
        amount = random.randint(100, 1000000)
    elif rand_num < 0.95:
        amount = random.randint(1000000, 5000000)
    else:
        amount = random.randint(5000000, 10000000)
    t = {
        "debitCustomer": from_customer,
        "creditCustomer": to_customer,
        "transaction": {
            "transactionId": str(uuid.uuid1())+str(int(time.time() * 1000000)),
            "amount": amount,
            "TransactionDate": faker.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S"),
            "description": faker.sentence(),
            "type": transaction_type
        },
        "ObservatoryId": 1
    }
    print("Transaction Generated " + t["transaction"]["transactionId"])
    # generate_row(t)

    response = post(t)
    if response.status_code == 200:
        print(response.json())
    print(response)
    return response

    # Token, RefreshToken = refresh_token(Token, RefreshToken)


print("Starting")

customers = [generate_customer() for _ in range(10000)]

for _ in range(30000):
    generate_transaction()

# generate_csv(rows)
# with open('transactions.json', 'w') as f:
#     json.dump(transactions, f)

print("Data generation complete.")
