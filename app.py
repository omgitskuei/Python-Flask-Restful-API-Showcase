from flask import Flask
from flask_restful import Api, Resource, reqparse

# instantiate firebase database
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
cred = credentials.Certificate("firebase-db-admin-key.json")
default_app = initialize_app(cred)
db = firestore.client()
# table named products
table_products = db.collection('products')

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help="name(str)", required=False)
parser.add_argument("price", type=int, help="price(int)", required=False)

@app.route('/')
def hello():
    return 'Hello World!'

# product list
class ProductList(Resource):
    # create new product
    def post(self):
        # get request's body
        new_product = parser.parse_args()
        print(new_product)
        table_products.document("xxx")                              # TO-DO
        return {
            'msg':'create multiple products, successful',
            'new_product' : new_product
        }
    
    # get all products
    def get(self):
        docs = table_products.get()
        product_list = []
        for doc in docs:
            product_list.append(doc.to_dict())
        return {
            'msg':'get products, successful',
            'all_products': product_list
        }

class Product(Resource):
    def get(self, pid):
        # get request's body
        # product = parser.parse_args()

        doc = table_products.document(pid).get()
        product = doc.to_dict()
        return {
            'msg':f'create single product id:{pid}, successful',
            'product' : product
        }
    
    def put(self, pid):
        # get request's body
        updated_product = parser.parse_args()

        table_products.document(pid).update(updated_product)
        return {
            'msg':f'update single product id:{pid}, successful',
            'updated_product' : updated_product
        }
    
    def delete(self, pid):

        table_products.document(pid).delete()
        return {
            'msg':f'delete single product id:{pid}, successful'
        }

api.add_resource(ProductList, '/api/all_products')
api.add_resource(Product, '/api/product/<pid>')


if __name__ == '__main__':
    app.run(debug=True)