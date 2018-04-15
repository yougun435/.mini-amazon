from flask import Flask, send_from_directory, request, Response
from pymongo import MongoClient
import re

client = MongoClient('localhost',27017)
db = client.miniamazonDB

app = Flask("mini-amazon", static_url_path="");

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')

@app.route('/products',methods=['POST','GET'])
def addProducts():

    if request.method == 'POST':
        if request.form['op_type'] == "insert":
            prod = {}
            prod['product name'] = request.form['name'];
            prod['product description'] = request.form['desc'];
            prod['cost'] = request.form['cost'];
            db.products.insert(prod)
            return Response("Product with details " + str(prod) + "successfully added........")

        elif request.form['op_type'] == "delete":
            result = db.products.delete_one(filter = {'product name' : request.form['name']})
            return Response("Product with name \t" + str(request.form['name']) + " \t and count: " + str(result.deleted_count) + " successfully deleted........")
        elif request.form['op_type']=='update':
            condition=dict()
            condition['name'] =  request.form['cur_name']

            update =dict()
            if request.form['name'] != '':
                update['product name']=request.form['name']
            if request.form['description'] != '':
                update['product description']=request.form['description']
            if request.form['cost'] !='':
                update['cost']=request.form['cost']

            db.products.update_one(filter=condition, update={'$set: update'})





    elif request.method == 'GET':
        matching_items = db.products.find({'product name': re.compile(request.args['name'], re.IGNORECASE)})

        if matching_items.count() <=0:
            return Response("Sorry!!! The product you searched is not found")
        matches = []
        for item in matching_items:
            matches.append(item)
        return Response("Product details are " + str(matches), mimetype="application/json")



if __name__ == '__main__':

 app.run(host='0.0.0.0', port=5000, debug = True)