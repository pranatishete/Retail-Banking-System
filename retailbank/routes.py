from flask import render_template,url_for,redirect, flash,request, session
from retailbank import app
from retailbank.forms import LoginForm, CreateCustomer, UpdateCustomer
from retailbank.forms import DeleteCustomer, CreateAccount, DeleteAccount
from retailbank.forms import CustomerSearch, AccountSearch, DepositMoney 
from retailbank.forms import WithdrawMoney, TransferMoney, AccountStatement
from retailbank.models import Customer, Admin,Account, Transaction
from retailbank import db
from sqlalchemy import and_


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and user.password_hash == form.password.data and user.stake_holder == 1:
            return redirect(url_for('dashboard_cashier'))
        if user and user.password_hash == form.password.data and user.stake_holder == 0:
            return redirect(url_for('dashboard_exec'))

    return render_template("home.html", form = form)

@app.route('/cashier/', methods=['GET', 'POST'])
def dashboard_cashier():
    return render_template("dashboard_cashier.html")

@app.route('/cashier/search', methods=['GET', 'POST'])
def customer_search():
    form = CustomerSearch()
    if form.validate_on_submit():
        if form.customer_ssn_id.data:
            session['customer_ssn_id'] = form.customer_ssn_id.data
            cust = Customer.query.filter_by(customer_ssn_id = form.customer_ssn_id.data).first()
            return render_template("cashier/customer_detail.html",c = cust)
        if form.customer_id.data:
            session['customer_id'] = form.customer_id.data
            cust = Customer.query.filter_by(customer_id = form.customer_id.data).first()
            return render_template("cashier/customer_detail.html",c = cust)
    return render_template("cashier/customer_search.html", form = form)

@app.route('/cashier/account', methods=['GET', 'POST'])
def account_search():
    form = AccountSearch()
    if form.validate_on_submit():
        if form.account_id.data:
            account = Account.query.filter_by(account_id = form.account_id.data).first()
            return render_template("cashier/account_detail.html",c = account)
        if form.customer_id.data:
            account = Account.query.filter_by(customer_id = form.customer_id.data).first()
            return render_template("cashier/account_detail.html",c = account)
    return render_template("cashier/account_search.html", form = form)

@app.route('/cashier/deposit/<int:id>', methods=['GET', 'POST'])
def deposit_money(id):
    acc_id = id
    a = Account.query.filter_by(account_id = acc_id).first()
    form = DepositMoney()
    if form.validate_on_submit():
        deposit_amount = form.deposit_amount.data
        a.balance = a.balance + deposit_amount
        transaction = Transaction(account_id = a.account_id,description='Deposit',amount=deposit_amount)
        db.session.add(transaction)
        db.session.commit()
        return render_template("cashier/account_detail.html",c = a)

    return render_template("cashier/deposit_money.html", form = form, a=a)

@app.route('/cashier/withdraw/<int:id>', methods=['GET', 'POST'])
def withdraw_money(id):
    acc_id = id
    a = Account.query.filter_by(account_id = acc_id).first()
    form = WithdrawMoney()
    if form.validate_on_submit():
        withdraw_money = form.withdraw_amount.data
        b = a.balance
        if (b-withdraw_money) >= 0:
            a.balance = a.balance - withdraw_money
            transaction = Transaction(account_id = a.account_id,description='Withdraw',amount=withdraw_money)
            db.session.add(transaction)
            db.session.commit()
            return render_template("cashier/account_detail.html",c = a)
        else:
            flash("insufficient balance. Try some smaller amount")
            return render_template("cashier/account_detail.html",c = a)
    return render_template("cashier/withdraw_money.html", form = form, a=a)

@app.route('/cashier/transfer', methods=['GET', 'POST'])
def transfer_money():
    form = TransferMoney()
    if form.validate_on_submit():
        customer_id = form.customer_id.data
        source_account_type = form.source_account_type.data
        target_account_type = form.target_account_type.data
        transfer_amount = form.transfer_amount.data
        source_account = Account.query.filter(and_(Account.customer_id == customer_id, Account.account_type == source_account_type)).first()
        target_account = Account.query.filter(and_(Account.customer_id == customer_id, Account.account_type == target_account_type)).first()
        if (source_account.balance - transfer_amount) < 0:
            flash("insufficient balance. Try some smaller amount")
        else:
            source_account.balance = source_account.balance - transfer_amount
            target_account.balance = target_account.balance + transfer_amount
            transaction = Transaction(account_id = source_account.account_id,description='Withdraw',amount=transfer_amount)
            transaction1 = Transaction(account_id = target_account.account_id,description='Deposit',amount=transfer_amount)
            db.session.add(transaction)
            db.session.add(transaction1)
            db.session.commit()
            return redirect(url_for("dashboard_cashier"))

    return render_template("cashier/transfer_money.html", form = form)

@app.route('/cashier/statement', methods=['GET', 'POST'])
def account_statement():
    form = AccountStatement()
    if form.validate_on_submit():
        account_id = form.account_id.data
        transactions = Transaction.query.filter_by(account_id = account_id)
        return render_template("cashier/statements.html", transactions = transactions)

    return render_template("cashier/account_statement.html", form = form)


@app.route('/executive', methods=['GET', 'POST'])
def dashboard_exec():
    return render_template("dashboard_exec.html")

@app.route('/executive/new', methods=['GET', 'POST'])
def new_customer():
    form = CreateCustomer()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(customer_ssn_id=form.customer_ssn_id.data,customer_name=form.customer_name.data,age=form.age.data,address=form.address.data,state=form.state.data,city=form.city.data,status = 'Pending',message='Welcome' )
        db.session.add(customer)
        db.session.commit()
        flash('New Customer added Successfully!', 'success')
        return redirect(url_for('dashboard_exec'))

    return render_template("executive/new_customer.html", form = form)

@app.route('/executive/view/<int:id>', methods=['GET', 'POST'])
def view_details(id):
    c = Customer.query.filter_by(customer_id = id).first()
    return render_template("executive/view_details.html",c = c)


@app.route('/executive/update', methods=['GET', 'POST'])
def update_customer():
    form = UpdateCustomer()
    if session['customer_id']:
        c = Customer.query.filter_by(customer_id = session['customer_id']).first()
    else:
        c = Customer.query.filter_by(customer_ssn_id = session['customer_ssn_id']).first()
    form.customer_ssn_id.data = c.customer_ssn_id
    form.customer_id.data = c.customer_id
    form.old_customer_name.data = c.customer_name
    form.old_address.data = c.address
    form.old_age.data = c.age    
    if form.validate_on_submit():
        if form.new_customer_name.data != c.customer_name:
            c.customer_name = form.new_customer_name.data
        if form.new_address.data != c.address:
             c.address = form.new_address.data
        if form.new_age.data != c.age:
             c.age = form.new_age.data
        db.session.commit()
        return redirect(url_for('dashboard_exec'))
    return render_template("executive/update_customer.html", form = form)

@app.route('/executive/search', methods=['GET', 'POST'])
def search_customer():
    form1 = CustomerSearch()
    session['customer_ssn_id'] = form1.customer_ssn_id.data
    session['customer_id'] = form1.customer_id.data

    if form1.validate_on_submit():
        return redirect(url_for('update_customer'))
    return render_template("executive/customer_search.html", form = form1)

@app.route('/executive/delete', methods=['GET', 'POST'])
def delete_customer():
    form = DeleteCustomer()
    if form.validate_on_submit():
        cust_id = form.customer_ssn_id.data
        cust = Customer.query.filter_by(customer_ssn_id = cust_id).first()
        if form.customer_ssn_id.data == cust.customer_ssn_id and form.customer_name.data == cust.customer_name and form.age.data == cust.age and form.address.data == cust.address:
            db.session.delete(cust)
            db.session.commit()
            return redirect(url_for('dashboard_exec'))
        else:
            flash("Customer Doesnt exist please fill the correct details!")
    return render_template("executive/delete_customer.html", form = form)

@app.route('/executive/new_account', methods=['GET', 'POST'])
def new_account():
    form = CreateAccount()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cust_account = Account(customer_id=form.customer_id.data,account_type=form.account_type.data,balance =form.deposit_amount.data,status = 'Active',message='Account Created')
        db.session.add(cust_account)
        db.session.commit()
        flash('New Account Created Successfully!', 'success')
        return redirect(url_for('dashboard_exec'))

    return render_template("executive/new_account.html", form = form)

@app.route('/executive/delete_account', methods=['GET', 'POST'])
def delete_account():
    form = DeleteAccount()
    if form.validate_on_submit():
        acc_id = form.account_id.data
        acc = Account.query.filter_by(account_id = acc_id).first()
        if form.account_type.data == acc.account_type: 
            db.session.delete(acc)
            db.session.commit()
            return redirect(url_for('dashboard_exec'))
        else:
            flash("Check Account type!")
        
    return render_template("executive/delete_account.html", form = form)

@app.route('/executive/account', methods=['GET', 'POST'])
def account_status():
    all_account = Account.query.all()
    for account in all_account:
        if account.customer_id is None:
            acc = Account.query.filter_by(customer_id = account.customer_id).first()
            db.session.delete(acc)
            db.session.commit()
            return redirect(url_for('dashboard_exec'))
    return render_template("executive/account_status.html",accounts=all_account)

@app.route('/executive/customer', methods=['GET', 'POST'])
def customer_status():
    all_cust = Customer.query.all()
    return render_template("executive/customer_status.html", customers = all_cust)

