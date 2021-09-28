from locust import task, between
from OdooLocust.OdooLocustUser import OdooLocustUser
import random
from faker import Faker
from faker_vehicle import VehicleProvider


fake = Faker()
fake.add_provider(VehicleProvider)

class Seller(OdooLocustUser):
    wait_time = between(0.1, 10)
    port = 8012
    database = "new12"
    login = "admin"
    password = "admin"
    protocol = "jsonrpc"

    @task(10)
    def read_partners(self):
        cust_model = self.client.get_model('res.partner')
        cust_ids = cust_model.search([('name', 'ilike', fake.last_name())])
        custs = cust_model.read(cust_ids)
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

    @task(5)
    def read_products(self):
        prod_model = self.client.get_model('product.product')
        ids = prod_model.search([('name', 'ilike', fake.vehicle_model())])
        prods = prod_model.read(ids)
        # create 1 product
        ids = categ_model.search([('name', '=', 'Vehicle')])
        if ids:
            parent_id = ids[0]
        else:
            parent_id = categ_model.create({'name': 'Vehicle',})
        for i in range(10):
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

    @task(20)
    def create_so(self):
        prod_model = self.client.get_model('product.product')
        cust_model = self.client.get_model('res.partner')
        so_model = self.client.get_model('sale.order')

        cust_ids = cust_model.search([
            ('customer', '=', True), 
            ('parent_id', '=', False), 
            '!', ('name', 'ilike', 'company')])
        cust_len = len(cust_ids)
        id1 = random.randint(0, cust_len-1)
        cust_id = cust_ids[id1]

        prod_ids = prod_model.search([
            ('product_tmpl_id.sale_ok', '=', True),
            ('product_tmpl_id.active', '=', True)])
        prod_len = len(prod_ids)
        id1 = random.randint(1, 20)

        order_line = []
        ids = []
        for i in range(id1):
            id2 = random.randint(0, prod_len-1)
            if id2 in ids:
                continue
            else:
                ids.append(id2)
            order_line.append((0, 0, {
                                'product_id': prod_ids[id2],
                                'product_uom_qty': random.randint(1, 10),
                                }))

        order_id = so_model.create({
            'partner_id': cust_id,
            'order_line': order_line,
        })

        so_model.action_confirm([order_id])  # Odoo 12
