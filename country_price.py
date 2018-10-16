import urllib2
import MySQLdb
import json


db = MySQLdb.connect(host="127.0.0.1",
                 user="root",
                 passwd="Marlboro",
                 db="numbeo")
db.set_character_set('utf8')


cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

countries = ["Afghanistan","Albania","Algeria","Andorra","Angola","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Bermuda","Bhutan","Bolivia","Bonaire","Bosnia%20And%20Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina%20Faso","Burundi","Cambodia","Cameroon","Canada","Cayman%20Islands","Chad","Chile","China","Colombia","Congo","Costa%20Rica","Croatia","Cuba","Curacao","Cyprus","Czech%20Republic","Denmark","Djibouti","Dominica","Dominican%20Republic","Ecuador","Egypt","El%20Salvador","Equatorial%20Guinea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea-Bissau","Guyana","Haiti","Honduras","Hong%20Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Ivory%20Coast","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Macao","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands","New%20Caledonia","New%20Zealand","Nicaragua","Nigeria","Norway","Oman","Pakistan","Palestinian%20Territory","Panama","Paraguay","Peru","Philippines","Poland","Portugal","Puerto%20Rico","Qatar","Reunion","Romania","Russia","Rwanda","Samoa","Saudi%20Arabia","Senegal","Serbia","Seychelles","Singapore","Sint%20Maarten","Slovakia","Slovenia","Solomon%20Islands","Somalia","South%20Africa","South%20Korea","Spain","Sri%20Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad%20And%20Tobago","Tunisia","Turkey","Turkmenistan","Uganda","Ukraine","United%20Arab%20Emirates","United%20Kingdom","United%20States","Uruguay","Uzbekistan","Vanuatu","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]
for _country in countries:
    # results = urllib2.urlopen('https://www.numbeo.com/api/country_prices?api_key=<API_KEY>&country=' + _country )
    results = urllib2.urlopen('https://www.numbeo.com/api/country_prices?api_key=<API_KEY>&country=' + _country + '&currency=USD')
    output = json.load(results)
    country = str(output['name'])
    valid_items = ['1', '3', '6', '8', '9', '11', '12', '17', '20', '24', '25', '26', '33', '40', '44', '60', '206', '224', '228', '105', '108', '110', '112', '114', '115', '118', '121']
    for price in output['prices']:
        if str(price['item_id']) in valid_items:
            if 'highest_price' not in price:
                price['highest_price'] = 'N/A'
            if 'lowest_price' not in price:
                price['lowest_price'] = 'N/A'
            cursor.execute("""INSERT INTO prices_usd (item_id, item, average_price_usd, country, highest_price_usd, lowest_price_usd) VALUES (%s, %s, %s, %s, %s, %s)""", (price['item_id'], str(price['item_name']), price['average_price'], country, price['highest_price'], price['lowest_price']))
    db.commit()

db.close()
