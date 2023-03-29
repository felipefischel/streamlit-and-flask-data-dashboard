from flask import Flask, jsonify, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields
import os

# Seting variables to connect to Database
host = os.environ['DB_HOST']
user = os.environ['DB_USER']
passw = os.environ['DB_PASS']
database = os.environ['DB_NAME']
port = os.environ['DB_PORT']

# ---------
# Token to access the APIs
auth_db = {
    os.environ['API_TOKEN']
}
# ---------

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'Felipes famous REST API with FLASK!',
    description = """
        This RESTS API is an API to built with FLASK
        and FLASK-RESTX libraries
        """,
    contact = "felipefischel@gmail.com",
    endpoint = "/api"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    )
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

# I create a function to execute the queries and return a JSON response.
# The function checks that the Authorization token is in the request header.
# It handles all errors and returns the corresponding error code.
def execute_query(query):
    try:
        if "Authorization" not in request.headers:
            return make_response(jsonify({"error": "unauthorized"}), 401)
        else:
            header = request.headers["Authorization"]
            token = header.split()[1]

            if token not in auth_db:
                return make_response(jsonify({"error": "unauthorized"}), 401)

        conn = connect()
        result = conn.execute(query).fetchall()
        disconnect(conn)
        return make_response(jsonify({'result': [dict(row) for row in result]}), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# ---------------- CUSTOMERS ----------------------------

customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api')
api.add_namespace(customers)

@customers.route("/customers")
class get_all_users(Resource):

    def get(self):
        get_all_users_query = """
            SELECT *
            FROM customers;"""
        return execute_query(get_all_users_query)

@customers.route("/customers/ages")
class get_customer_by_age(Resource):

    def get(self):
        get_customer_by_age_query = """
            SELECT *
            FROM customers_by_age;"""
        return execute_query(get_customer_by_age_query)

@customers.route("/customers/ages/spent")
class get_amount_spent_age(Resource):

    def get(self):
        get_amount_spent_age_query = """
            SELECT *
            FROM age_group_spenditure;"""
        return execute_query(get_amount_spent_age_query)

@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
class select_customer(Resource):

    def get(self, id):
        id = str(id)
        select_customer_query = """
            SELECT *
            FROM customers
            WHERE customer_id = '{0}';""".format(id)
        return execute_query(select_customer_query)

# ---------------- ARTICLES ----------------------------

articles = Namespace('articles',
    description = 'All operations related to articles',
    path='/api')
api.add_namespace(articles)

@articles.route("/articles")
class get_all_articles(Resource):

    def get(self):
        get_all_articles_query = """
            SELECT *
            FROM articles
            LIMIT 1000;"""
        return execute_query(get_all_articles_query)

@articles.route("/articles/top/products")
class get_top_products(Resource):

    def get(self):
        get_top_products_query = """
            SELECT *
            FROM product_count;"""
        return execute_query(get_top_products_query)

@articles.route("/articles/top/colors")
class get_top_colors(Resource):

    def get(self):
        get_top_colors_query = """
            SELECT *
            FROM color_count;"""
        return execute_query(get_top_colors_query)

@articles.route("/articles/sold/count")
class get_top_articles_sold(Resource):

    def get(self):
        get_top_articles_sold_query = """
            SELECT *
            FROM qty_products_sold_by_type;"""
        return execute_query(get_top_articles_sold_query)

@articles.route("/articles/sold/revenue")
class get_top_articles_sold_rev(Resource):

    def get(self):
        get_top_articles_sold_rev_query = """
            SELECT *
            FROM revenue_by_product_type;"""
        return execute_query(get_top_articles_sold_rev_query)

@articles.route("/articles/<string:id>")
@articles.doc(params = {'id': 'The ID of the article'})
class select_article(Resource):

    def get(self, id):
        id = str(id)
        select_article_query = """
            SELECT *
            FROM articles
            WHERE article_id = '{0}';""".format(id)
        return execute_query(select_article_query)

# ---------------- TRANSACTIONS ----------------------------

transactions = Namespace('transactions',
    description = 'All operations related to transactions',
    path='/api')
api.add_namespace(transactions)

@transactions.route("/transactions")
class get_all_transactions(Resource):

    def get(self):
        get_all_transactions_query = """
            SELECT *
            FROM transactions
            LIMIT 1000;
            """
        return execute_query(get_all_transactions_query)

@transactions.route("/transactions/revenue/<string:start_date>/<string:end_date>")
@transactions.doc(params = {'start_date': 'The start date', 'end_date': 'The end date'})
class get_transactions_rev_by_date(Resource):

    def get(self, start_date, end_date):
        get_transactions_rev_by_date_query = """
            SELECT *
            FROM transactions_per_day_by_price_and_channel
            WHERE t_dat BETWEEN '{0}' AND '{1}'""".format(start_date, end_date)
        return execute_query(get_transactions_rev_by_date_query)

@transactions.route("/transactions/avg_price/<string:start_date>/<string:end_date>")
@transactions.doc(params = {'start_date': 'The start date', 'end_date': 'The end date'})
class get_transactions_avgprice_by_date(Resource):

    def get(self, start_date, end_date):
        get_transactions_avgprice_by_date_query = """
            SELECT *
            FROM transactions_per_day_avg
            WHERE t_dat BETWEEN '{0}' AND '{1}'""".format(start_date, end_date)
        return execute_query(get_transactions_avgprice_by_date_query)

if __name__ == '__main__':
    app.run(debug = True, port = 5005)
