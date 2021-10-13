import odoolib
import random
import datetime

po_num = 100
line_num = 56
host = "localhost"
port = 8012
database = "new12"
login = "admin"
password = "admin"
protocol = "jsonrpc"

connection = odoolib.get_connection(hostname=host, database=database, \
    login=login, password=password, protocol=protocol, port=port)

prod_model = connection.get_model('product.product')
supl_model = connection.get_model('res.partner')
po_model = connection.get_model('purchase.order')
line_model = connection.get_model('purchase.order.line')
pick_model = connection.get_model('stock.picking.type')

for i in range(po_num):
    supl_ids = supl_model.search([
        ('supplier', '=', True), 
        ('parent_id', '=', False), 
        ('is_company', '=', True),
        ])
    id1 = random.randint(0, len(supl_ids)-1)
    supl_id = supl_ids[id1]

    prod_ids = prod_model.search([
        ('product_tmpl_id.purchase_ok', '=', True),
        ('product_tmpl_id.active', '=', True)])

    prod_len = len(prod_ids)
    id2 = random.randint(0, prod_len-1)
    prod_id = prod_ids[id2]
    prod = prod_model.read([prod_id])
    
    pick_ids = pick_model.search([('code','=','incoming')])
    if len(pick_ids) > 1:
        id3 = random.randint(0, len(pick_ids)-1)
    else:
        id3 = 0

    order_id = po_model.create({
        'partner_id': supl_id,
        'picking_type_id': pick_ids[id3],
        'order_line': [(0, 0, {
            'product_id': prod_id,
            'name': prod[0]['name'],
            'date_planned': datetime.datetime.now().strftime('%Y-%m-%d'),
            'product_uom': prod[0]['uom_po_id'][0],
            'price_unit': prod[0]['standard_price'],
            'product_qty': random.randint(1,123)}
            )]
        })
    # po = po_model.read([order_id])
    # print(po[0]['name'])

    ids = [id2]
    for k in range(random.randint(1,line_num)):
        id2 = random.randint(0, prod_len-1)
        if id2 in ids:
            continue
        else:
            ids.append(id2)
        prod_id = prod_ids[id2]
        prod = prod_model.read([prod_id])
        line_model.create({
            'order_id': order_id,
            'product_id': prod_id,
            'name': prod[0]['name'],
            'date_planned': datetime.datetime.now().strftime('%Y-%m-%d'),
            'product_uom': prod[0]['uom_po_id'][0],
            'price_unit': prod[0]['standard_price'],
            'product_qty': random.randint(1,123),
            })
    # confirm purchase
    # if random.randint(0,123)%2 == 0:
    po_model.button_confirm([order_id])
