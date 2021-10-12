import odoolib
import random


so_num = 1   # number of sale orders
line_num = 1 # maximum number of lines per sale order
host = "localhost"
port = 8012
database = "new12"
login = "admin"
password = "admin"
protocol = "jsonrpc"

connection = odoolib.get_connection(hostname=host, database=database, \
    login=login, password=password, protocol=protocol, port=port)

# 10.000.000 sale orders
so_model = connection.get_model('sale.order')
line_model = connection.get_model('sale.order.line')
cust_model = connection.get_model('res.partner')
prod_model = connection.get_model('product.product')
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
                            'product_uom_qty': random.randint(1, 12),
                            })],
        })
    ids = [id2]
    for k in range(random.randint(1, line_num)):
        id2 = random.randint(0, prod_len-1)
        if id2 in ids:
            continue
        else:
            ids.append(id2)
        line_model.create({
            'order_id': order_id,
            'product_id': prod_ids[id2],
            'product_uom_qty': random.randint(1, 12),
            })

    if random.randint(0, 123)%2 == 0:
        so_model.action_confirm([order_id])  # Odoo 12
