from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, RadioField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
import black

class LoginForm(FlaskForm):
	username = StringField("Username", validators = [DataRequired(), Length(min = 2, max = 20)])
	password = PasswordField("Password", validators = [DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Sign In")


class CreateCustomer(FlaskForm):
	customer_ssn_id = IntegerField("Customer SSN ID", validators=[DataRequired()])
	customer_name  = StringField("Customer Name ",validators = [DataRequired("Please enter your name.")])
	age = IntegerField("Age",validators=[DataRequired()])
	address = TextAreaField("Address",validators=[DataRequired(),Length(max=200)])  
	state = SelectField('Select State', choices = [('java', 'Java'),('py', 'Python')])  
	city = SelectField('Select City', choices = [('java', 'Java'),('py', 'Python')])  
	create = SubmitField("Submit")


class UpdateCustomer(FlaskForm):
	customer_ssn_id  =  IntegerField("Customer SSN ID",validators=[DataRequired()])
	customer_id = IntegerField("Customer ID")
	old_customer_name =  StringField("Customer Name")
	new_customer_name =  StringField("Enter Changed Customer Name ",validators=[DataRequired("Please enter your name.")])
	old_address = TextAreaField("Address")  
	new_address = TextAreaField("Address",validators=[DataRequired()])  
	old_age = IntegerField("Age")
	new_age = IntegerField("Enter Age",validators=[DataRequired()])
	update = SubmitField("Update")


class DeleteCustomer(FlaskForm):
	customer_ssn_id = IntegerField("Customer SSN ID",validators=[DataRequired()])
	customer_name = StringField("Customer Name ",validators=[DataRequired("Please enter your name.")])
	age = IntegerField("Age",validators=[DataRequired()])
	address = TextAreaField("Address",validators=[DataRequired(),Length(max=200)]) 
	delete = SubmitField("Confirm Delete")
	cancel = SubmitField("Cancel")


class CreateAccount(FlaskForm):
	customer_id = IntegerField("Customer ID")
	account_type = SelectField('Select Account Type', choices = [('savings', 'Savings'),('current', 'Current')])
	deposit_amount =  IntegerField("Deposit amount",validators=[DataRequired()])
	create_account = SubmitField("Submit")


class DeleteAccount(FlaskForm):
	account_id = IntegerField("Account ID",validators=[DataRequired()])
	account_type = SelectField('Select Account Type', choices = [('savings', 'Savings'),('current', 'Current')])
	delete_account = SubmitField("Delete Account")

class CustomerSearch(FlaskForm):
	customer_ssn_id = IntegerField("Customer SSN ID")
	customer_id = IntegerField("Customer ID")
	customer_search = SubmitField("View")

class AccountSearch(FlaskForm):
	account_id = IntegerField("Account ID")
	customer_id = IntegerField("Customer ID")
	account_search = SubmitField("View")

class DepositMoney(FlaskForm):
	deposit_amount = IntegerField("Deposit amount",validators=[DataRequired()])
	deposit = SubmitField("Deposit")

class WithdrawMoney(FlaskForm):	
	withdraw_amount = IntegerField("Withdraw amount",validators=[DataRequired()])
	withdraw =  SubmitField("Withdraw")

class TransferMoney(FlaskForm):
	customer_id = IntegerField("Customer ID")
	source_account_type = SelectField('Select Account Type', choices = [('savings', 'Savings'),('current', 'Current')])
	target_account_type = SelectField('Select Account Type', choices = [('savings', 'Savings'),('current', 'Current')])
	transfer_amount = IntegerField("Transfer amount",validators=[DataRequired()])
	transfer = SubmitField("Transfer")

class AccountStatement(FlaskForm):
	account_id = IntegerField("Account ID",validators=[DataRequired()])
	option = RadioField('', choices = [(0,'Last Number of Transactions'),(1,'Start-End Dates')])  
	no_of_transactions = SelectField("Last 10 Transactions Only")
	start_date = DateField('Start Date',format='%d-%m-%Y')
	end_date =  DateField('End Date',format='%d-%m-%Y')
	get_statement = SubmitField("Get Statement")