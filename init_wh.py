import odoolib
import random
from faker import Faker

wh_num = 10  # number of warehouses
host = "localhost"
port = 8008
database = "new8"
login = "admin"
password = "admin"
protocol = "xmlrpc"


fake = Faker()


connection = odoolib.get_connection(hostname=host, database=database, \
    login=login, password=password, protocol=protocol, port=port)

# 1.000.000 whomers
wh_model = connection.get_model('stock.warehouse')
loc_model = connection.get_model('stock.location')
for i in range(wh_num):
    # create 1 warehouse
    if i > 999:
        break
    wh_name = 'WH' + str(i).zfill(3)
    # print(wh_name)
    wh_ids = wh_model.search([('code','=',wh_name)])
    if not wh_ids:
        wh_id = wh_model.create({
            'name': wh_name,
            'code': wh_name, 
        })
    wh_ids = loc_model.search([('name','=',wh_name)])
    if wh_ids:
        stock_ids = loc_model.search([('name','=','Stock'), ('location_id','=',wh_ids[0])])
        if stock_ids:
            stock_id = stock_ids[0]
        else:
            continue
    else:
        continue
    # create 1 corridor
    for j in range(wh_num):
        cor_name = 'Corridor' + str(j).zfill(3)
        # print(cor_name)
        cor_ids = loc_model.search([('name','=',cor_name), ('location_id','=',stock_id)])
        if cor_ids:
            cor_id = cor_ids[0]
        else:
            cor_id = loc_model.create({
                'name': cor_name,
                'location_id': stock_id,
                'posx': j,
                })
        for k in range(wh_num):
            sh_name = 'Shelf' + str(k).zfill(3)
            # print(sh_name)
            sh_ids = loc_model.search([('name','=',sh_name), ('location_id','=',cor_id)])
            if sh_ids:
                sh_id = sh_ids[0]
            else:
                sh_id = loc_model.create({
                    'name': sh_name,
                    'location_id': cor_id,
                    'posx': j,
                    'posy': k,
                    })
            for l in range(wh_num):
                he_name = 'Height' + str(l).zfill(3)
                # print(he_name)
                he_ids = loc_model.search([('name','=',he_name), ('location_id','=',sh_id)])
                if not he_ids:
                    he_id = loc_model.create({
                        'name': he_name,
                        'location_id': sh_id,
                        'posx': j,
                        'posy': k,
                        'posz': l,
                        })
