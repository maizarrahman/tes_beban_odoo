import odoolib
import random
from faker import Faker
from faker_vehicle import VehicleProvider

cust_num = 10   # number of customers
host = "localhost"
port = 8012
database = "new12"
login = "admin"
password = "admin"
protocol = "jsonrpc"


fake = Faker()
fake.add_provider(VehicleProvider)


connection = odoolib.get_connection(hostname=host, database=database, \
    login=login, password=password, protocol=protocol, port=port)

# 1.000.000 customers
cust_model = connection.get_model('res.partner')
for i in range(cust_num):
    # create 1 customer
    country_id = random.randint(0,252)
    phone1 = '+' + str(country_id+1)
    name1 = fake.first_name() + ' ' + fake.last_name()
    domain = fake.domain_name(levels=1)
    cust_id = cust_model.create({
        'name': name1,
        'street': fake.street_address(),
        'phone': phone1 + fake.numerify(text=' ## ###-####'),
        'function': fake.job(),
        'email': name1.lower().replace(' ','.') + '@' + domain,
        'website': 'https://www.' + domain,
        'city': fake.city(),
        'country_id': country_id,
        'mobile': phone1 + ' ' + fake.numerify(text='###-####-####'),
    })
