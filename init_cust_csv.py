import random
import csv
from faker import Faker
from faker_vehicle import VehicleProvider


cust_num = 10000   # number of customers
cust_filename = 'customer.csv'

fake = Faker()
fake.add_provider(VehicleProvider)

f = open(cust_filename, 'w')
writer = csv.writer(f)
row = ["name","street","phone","function","email","website","city","mobile"]
writer.writerow(row)
f.flush()

for i in range(cust_num):
    # create 1 customer
    country_id = random.randint(0,252)
    phone1 = '+' + str(country_id+1)
    name1 = fake.first_name() + ' ' + fake.last_name()
    domain = fake.domain_name(levels=1)
    row = [
        name1,
        fake.street_address(),
        phone1 + fake.numerify(text=' ## ###-####'),
        fake.job(),
        name1.lower().replace(' ','.') + '@' + domain,
        'https://www.' + domain,
        fake.city(),
        phone1 + ' ' + fake.numerify(text='###-####-####'),
    	]
    writer.writerow(row)
    f.flush()
f.close()
