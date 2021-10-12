import odoolib
import random
from faker import Faker
from faker_vehicle import VehicleProvider


prod_num = 1000   # number of products
host = "localhost"
port = 8008
database = "new8"
login = "admin"
password = "admin"
protocol = "xmlrpc"

fake = Faker()
fake.add_provider(VehicleProvider)

connection = odoolib.get_connection(hostname=host, database=database, \
    login=login, password=password, protocol=protocol, port=port)

# 100.000 products
prod_model = connection.get_model('product.product')
categ_model = connection.get_model('product.category')
ids = categ_model.search([('name', '=', 'Vehicle')])
if ids:
    parent_id = ids[0]
else:
    parent_id = categ_model.create({'name': 'Vehicle',})
for i in range(prod_num):
    prod = fake.vehicle_object()
    # create 1 product category if not exist
    # print(prod)
    ids = categ_model.search([('name', '=', prod['Category'])])
    if ids:
        categ_id = ids[0]
    else:
        categ_id = categ_model.create({
            'name': prod['Category'],
            'parent_id': parent_id,
            })
    # create 1 product
    price = round(random.uniform(1000.0, 9999.99), 2)
    prod_id = prod_model.create({
        'name': prod['Make'] + ' ' + prod['Model'] + ' ' + str(prod['Year']),
        'categ_id': categ_id,
        'type': 'product',
        'list_price': price,
        'standard_price': round(price * random.uniform(0.5, 0.9), 2),
        'default_code': fake.bothify(text='????-####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        })
