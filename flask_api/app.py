from flask import Flask,request,jsonify
from flask_sqlalchemy import  SQLAlchemy 
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import os

app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_ssn_id = db.Column(db.Integer, unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    last_updated = db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
    #children = relationship("Account")

    def __init__(self,customer_id,customer_ssn_id,customer_name,age,address,state,city,status,message,last_updated):
        self.customer_id = customer_id
        self.customer_ssn_id = customer_ssn_id
        self.customer_name = customer_name
        self.age = age
        self.address = address
        self.state = state
        self.city = city
        self.status = status
        self.message = message
        self.last_updated = last_updated


class CustomerSchema(ma.Schema):
	class Meta:
		fields = ('customer_id','customer_ssn_id','customer_name','age','address','state','city','status','message','last_updated')


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)



#create a customer
@app.route('/customer',methods=['POST'])
def add_customer():
	customer_id = request.json['customer_id']
	customer_ssn_id = request.json['customer_ssn_id']
	customer_name = request.json['customer_name']
	age = request.json['age']
	address = request.json['address']
	state = request.json['state']
	city = request.json['city']
	status = request.json['status']
	message =  request.json['message']
	last_updated = request.json['last_updated']

	new_customer = Customer(customer_id,customer_ssn_id,customer_name,age,address,state,city,status,message,last_updated)
	db.session.add(new_customer)
	db.session.commit()
	return customer_schema.jsonify(new_customer)



@app.route('/customer',methods = ['GET'])
def get_customers():
	all_customers = Customer.query.all()
	result = customers_schema.dump(all_customers)
	return jsonify(result)


@app.route('/customer/<id>',methods = ['GET'])
def get_customer(id):
	customer = Customer.query.get(id)
	return customer_schema.jsonify(customer)

@app.route('/customer/<id>',methods = ['PUT','POST'])
def update_customer(id):
	customer = Customer.query.get(id)
	customer_id = request.json['customer_id']
	customer_ssn_id = request.json['customer_ssn_id']
	customer_name = request.json['customer_name']
	age = request.json['age']
	address = request.json['address']
	state = request.json['state']
	city = request.json['city']
	status = request.json['status']
	message =  request.json['message']
	last_updated = request.json['last_updated']

	customer.name = customer_name
	customer.age = age
	customer.address = address
	customer.state = state
	customer.city = city
	customer.last_updated = datetime.utcnow

	db.session.commit()

	return customer_schema.jsonify(customer)


@app.route('/customer/<id>',methods = ['DELETE'])
def delete_customer(id):
	customer = Customer.query.get(id)
	db.session.delete(customer)
	db.session.commit()


	return customer_schema.jsonify(customer)



if __name__ == '__main__':
	app.run(debug=True)

