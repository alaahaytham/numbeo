import urllib2
import MySQLdb
import json
import sys

db = MySQLdb.connect(host="127.0.0.1",
                 user="root",
                 passwd="Marlboro",
                 db="numbeo")
db.set_character_set('utf8')


cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

cursor = db.cursor()

countries = ["Afghanistan","Albania","Algeria","Angola","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Belarus","Belgium","Bhutan","Bolivia","Bosnia%20And%20Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina%20Faso","Burundi","Cambodia","Cameroon","Canada", "Chad","Chile","China","Colombia","Congo","Costa%20Rica","Croatia","Cuba","Cyprus","Czech%20Republic","Denmark","Djibouti","Ecuador","Egypt","El%20Salvador","Equatorial%20Guinea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Greenland","Guatemala","Guinea-Bissau","Haiti","Honduras","Hong%20Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Ivory%20Coast","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New%20Zealand","Nicaragua","Nigeria","Norway","Oman","Pakistan","Palestinian%20Territory","Panama","Paraguay","Peru","Philippines","Poland","Portugal","Puerto%20Rico","Qatar","Romania","Russia","Rwanda","Saudi%20Arabia","Senegal","Serbia","Seychelles","Singapore","Slovakia","Slovenia","Somalia","South%20Africa","South%20Korea","Spain","Sri%20Lanka","Sudan","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Tunisia","Turkey","Turkmenistan","Uganda","Ukraine","United%20Arab%20Emirates","United%20Kingdom","United%20States","Uruguay","Uzbekistan","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

items = {}
item = []


sql = "SELECT distinct(item_id), item from prices"
cursor.execute(sql)
results = cursor.fetchall()
for result in results:
    item.append({ 'id': int(result[0]), 'name': result[1] })

items['items'] = item

print items

entries = {}
entry = []
for country in countries:
    sql = "SELECT prices_usd.item_id, prices_usd.item, TRUNCATE(prices_usd.average_price_usd, 2) as average_price_usd, TRUNCATE(prices_usd.lowest_price_usd, 2) as lowest_price_usd, TRUNCATE(prices_usd.highest_price_usd, 2) as highest_price_usd, TRUNCATE(prices.average_price, 2) as average_local_price, TRUNCATE(prices.lowest_price, 2) as lowest_local_price, TRUNCATE(prices.highest_price, 2) as highest_local_price left join prices on prices.id = prices_usd.id where prices.country = '"+ country +"' group by prices_usd.item order by prices_usd.item_id"
    cursor.execute(sql)
    results = cursor.fetchall()

    for result in results:
        entry.append({
            'item_id': int(result[0]),
            'name': country,
            'average_price_usd': result[2],
            'lowest_price_usd': result[3],
            'highest_price_usd': result[4],
            'average_local_price': result[5],
            'lowest_local_price': result[6],
            'highest_local_price': result[7]
        })
    entries['data'] = entry

finals = {}
final = []

# print entries

for i in items['items']:
    print i
    for e in entries['data']:
        if i['id'] == e['item_id']:
            final.append(e)
    finals[i['name']] = final

f = open('output.json', 'w')
print >> f, finals


print finals


db.commit()
db.close()
