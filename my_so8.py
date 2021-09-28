from locust import task, between
# from OdooLocust.OdooLocustUser import OdooLocustUser
import random
from faker import Faker
import odoolib
import time
import sys
from locust import HttpUser, events
if sys.version_info >= (3, 0, 0):
    from xmlrpc.client import ServerProxy
else:
    from xmlrpclib import ServerProxy
from faker_vehicle import VehicleProvider


def send(self, service_name, method, *args):
    url = '%s/%s' % (self.url, service_name)
    service = ServerProxy(url)

    if service_name == "object" and method == "execute_kw":
        call_name = "%s : %s" % args[3:5]
    else:
        call_name = '%s : %s' % (service_name, method)
    start_time = time.time()
    try:
        # res = odoolib.json_rpc(self.url, "call", {"service": service_name, "method": method, "args": args})
        res = getattr(service, method)(*args)
    except Exception as e:
        total_time = int((time.time() - start_time) * 1000)
        events.request_failure.fire(request_type="Odoo XmlRPC", name=call_name, response_time=total_time, response_length=0, exception=e)
        raise e
    else:
        total_time = int((time.time() - start_time) * 1000)
        events.request_success.fire(request_type="Odoo XmlRPC", name=call_name, response_time=total_time, response_length=sys.getsizeof(res))
        return res


odoolib.XmlRPCConnector.send = send
odoolib.XmlRPCSConnector.send = send


class OdooLocustUserXml(HttpUser):
    port = 8008
    database = "new8"
    login = "admin"
    password = "admin"
    protocol = "xmlrpc"
    user_id = -1

    def on_start(self):
        user_id = None
        if self.user_id and self.user_id > 0:
            user_id = self.user_id
        self.client = odoolib.get_connection(hostname=self.host,
                                             port=self.port,
                                             database=self.database,
                                             login=self.login,
                                             password=self.password,
                                             protocol=self.protocol,
                                             user_id=user_id)
        self.client.check_login(force=False)


fake = Faker()
fake.add_provider(VehicleProvider)

class Seller(OdooLocustUserXml):
    wait_time = between(0.1, 10)
    # port = 8008
    # database = "new8"
    # login = "admin"
    # password = "admin"
    # protocol = "xmlrpc"

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
            ])
        cust_len = len(cust_ids)
        id1 = random.randint(0, cust_len-1)
        cust_id = cust_ids[id1]

        prod_ids = prod_model.search([
            ('product_tmpl_id.sale_ok', '=', True),
            ('product_tmpl_id.active', '=', True),
            ])
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

        if random.randint(0, 1234)%2 == 0:
            so_model.action_button_confirm([order_id])  # Odoo 8
