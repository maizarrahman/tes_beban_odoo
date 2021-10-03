import csv
import random
from faker import Faker
from faker_vehicle import VehicleProvider


prod_num = 10000  # number of products
prod_filename = 'product.csv'

fake = Faker()
fake.add_provider(VehicleProvider)

# 100.000 products
f = open(prod_filename, 'w')
writer = csv.writer(f)
row = ["name","type","list_price","standard_price","default_code","image_medium"]
writer.writerow(row)
f.flush()

for i in range(prod_num):
    prod = fake.vehicle_object()
    # create 1 product
    price = round(random.uniform(1000.0, 9999.99), 2)
    row = [
        prod['Make'] + ' ' + prod['Model'] + ' ' + str(prod['Year']),
        'product',
        price,
        round(price * random.uniform(0.5, 0.9), 2),
        fake.bothify(text='????-####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        ]
    writer.writerow(row)
    f.flush()
