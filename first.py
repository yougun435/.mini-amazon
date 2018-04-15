from flask import Flask, send_from_directory, request, Response
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.miniamazonDB


app = Flask("mini-amazon", static_url_path="");

indexPosition = 0
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('staticHtmlFiles',"index.html")



@app.route('/products', methods=['POST','GET'])
def addProducts():

    if request.method == 'POST':
        prod = {}
        prod['product name'] = request.form['name'];
        prod['product description'] = request.form['desc'];
        prod['cost'] = request.form['cost'];
        db.products.insert(prod)
        return Response("Product with details " + str(prod) + "successfully added........")

    elif request.method == 'GET':
        matching_items = db.products.find({'product name': {"$regex": request.args['name']}})

        if matching_items.count() <=0:
            return Response("Sorry!!! The product you searched is not found")
        matches = []
        for item in matching_items:
            matches.append(item)
        return Response("Product details are " + str(matches), mimetype="application/json")




@app.route('/listProducts', methods=['GET'])
def listProducts():
    count = 0
    allItems = db.products.find()
    if allItems.count() > 0:
        matches = []
        for item in allItems:
            matches.append(item)
        return Response("Product details are " + str(matches) , mimetype="application/json" )
    else:
        return Response("Empty List! No data found.", mimetype="text/plain")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
