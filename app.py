from flask import Flask, request, make_response
import mysql.connector

app = Flask(__name__)

# @app.route('/customers', methods = ['GET']) templte app.route
# def getCustomers():

if __name__ == 'main':
    app.run()