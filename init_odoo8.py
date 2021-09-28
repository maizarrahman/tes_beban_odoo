import odoolib
import random
from faker import Faker
from faker_vehicle import VehicleProvider

cust_num = 10   # number of customers
prod_num = 10   # number of products
so_num   = 10   # number of sale orders
line_num = 10   # maximum number of lines in a sale order

fake = Faker()
fake.add_provider(VehicleProvider)


connection = odoolib.get_connection(hostname="localhost", database="new8", \
    login="admin", password="admin", protocol="xmlrpc", port=8008)

# 1.000.000 customers
cust_model = connection.get_model('res.partner')
for i in range(cust_num):
    # create 1 customer
    country_id = random.randint(1,99)
    phone1 = '+' + str(country_id)
    phone2 = phone1 + fake.numerify(text=' ## ') + fake.numerify(text='###')
    name1 = fake.name().replace('Mr. ','').replace('Mrs. ','')
    domain = fake.domain_name(levels=1)
    cust_id = cust_model.create({
        'name': name1,
        'street': fake.street_address(),
        'phone': phone2 + fake.numerify(text='-####'),
        'job': fake.job(),
        'email': name1.lower().replace(' ','.') + '@' + domain,
        'website': 'https://www.' + domain,
        'city': fake.city(),
        'country_id': country_id,
        'mobile': phone1 + ' ' + fake.numerify(text='###-####-####'),
        'fax': phone2 + fake.numerify(text='-####'),
    })

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
    prod_id = prod_model.create({
        'name': prod['Make'] + ' ' + prod['Model'] + ' ' + str(prod['Year']),
        'categ_id': categ_id,
        'type': 'product',
        'list_price': round(random.uniform(0.0, 1.0)*10000.0, 2),
        'standard_price': round(random.uniform(0.0, 1.0)*10000.0, 2),
        'default_code': fake.bothify(text='????-####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        })

# 10.000.000 sale orders
so_model = connection.get_model('sale.order')
for i in range(so_num):
    cust_ids = cust_model.search([
        ('customer', '=', True), 
        ('parent_id', '=', False), 
        ])
    cust_len = len(cust_ids)
    id1 = random.randint(0, cust_len-1)
    cust_id = cust_ids[id1]

    prod_ids = prod_model.search([
        ('product_tmpl_id.sale_ok', '=', True),
        ('product_tmpl_id.active', '=', True),
        ])
    prod_len = len(prod_ids)

    id2 = random.randint(0, prod_len-1)
    order_id = so_model.create({
        'partner_id': cust_id,
        'order_line': [(0, 0, {
                            'product_id': prod_ids[id2],
                            'product_uom_qty': random.randint(1, 123),
                            })],
        })
    ids = [id2]
    for i in range(random.randint(1, line_num)):
        id2 = random.randint(0, prod_len-1)
        if id2 in ids:
            continue
        else:
            ids.append(id2)
        line_model.create({
            'order_id': order_id,
            'product_id': prod_ids[id2],
            'product_uom_qty': random.randint(1, 123),
            })

    if random.randint(0, 1234)%2 == 0:
        so_model.action_button_confirm([order_id])  # Odoo 8
