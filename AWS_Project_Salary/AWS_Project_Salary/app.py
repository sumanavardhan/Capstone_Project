# -*- coding: utf-8 -*-
"""
Created on Tue Jue 6 16:39:56 2023

@author: Sumana Chittamuri
"""

from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import boto3
from flask import g

app = Flask(__name__)

boto3.setup_default_session(region_name='us-east-1')

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id="ASIA2X5HZ7YK5DA7JYTR",
        aws_secret_access_key=  "BPv0+uiZ5BlEEJt6jXQKZ19BiZEJcTZSXzQ6qb+/",
        aws_session_token= "IQoJb3JpZ2luX2VjEBoaCXVzLWVhc3QtMSJHMEUCIQDAxSntZsTlLy3sBS3WxNp1ZGMwr5ZAaK99mlXkiu9jVgIgXxdp5kc45GtsNk8uJBzIIo5nXs8tVrUqrcEkQ87sAZIq0wEIYxAAGgw3Mzg1NDk0MzE4MjkiDLocx7QpamP26QO+kyqwAbr0hX/7NcILgIxofNkJ70pJPC9hoAEkeKvfwSSrWwtiTfBjQR8AOFsitV6lmh2jqPiy3T4WYc399xJACYMNi6T24q31Dk4yttQMOGhj2HDWiRWpb2vzJyuRASiNdAYHEqeHQSbxy2pAxQyyl4ljzDzNQbtfk5mXM/LEraleEThBukEfCurM04OR5AYIOQFcgofCUc7rOmzSuu9yScA3O4V0GPTnntTtShZhHTij86r9MJj6gqQGOpgB33CvpZAqfTK2OnDxvGQWBVHO6dOPoaOy4apa7zI0aW1jqmqyGTnh3Aj/xmhD8/jvofu+Eks/FaZI8t2WBVdX83GuVucq8oLAwBEwn9v29UEx+LnmNcde9cDDZbY3Mvgx6UHHOzxYyVFILcl0TcJCpBZ1l3NQTLmxf/93qgqfzkPF03w5Uetc8yt4txzdtwHQG6RHifbWBlg="
      )

dynamodbEmployee = boto3.resource('dynamodb',
                    aws_access_key_id="AKIAQENB5424S2QCDW2X",
                    aws_secret_access_key=  "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",
                    )

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['get', 'post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table('userdata')

        table.put_item(
                Item={
        'name': name,
        'email': email,
        'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"

        return render_template('login.html',msg = msg)
    return render_template('index.html')

@app.route('/submission', methods=['GET', 'POST'])
def submission():
    if request.method == 'POST':

        id = str(get_latest_id() + 1)
        age = request.form['age']
        gender = request.form['gender']
        education_level = request.form['education_level']
        job_title = request.form['job_title']
        years_of_experience = request.form['years_of_experience']
        salary = request.form['salary']

        table2 = dynamodbEmployee.Table('Salary')
        # Generate a unique ID starting from 7000

        table2.put_item(
            Item={
                'id' : id,
                'Age': age,
                'Gender': gender,
                'Education Level': education_level,
                'Job Title': job_title,
                'Years of Experience': years_of_experience,
                'Salary': salary
            }
        )

    return render_template('new_entry.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        id = request.form['id']
        table2 = dynamodbEmployee.Table('Salary')
        response = table2.get_item(Key={'id': id})
        item = response.get('Item')

        if item:
            return render_template('query_data.html', result=item)
        else:
            msg = "No data found for the provided ID."
            return render_template('query_data.html', msg=msg)

    return render_template('query_data.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#generates id
def get_latest_id():
    # Check if the latest ID is already stored in the Flask application context
    if 'latest_id' in g:
        return g.latest_id

    # Retrieve the latest ID from the database
    response = dynamodbEmployee.Table('Salary').scan(
        Select='COUNT'
    )
    latest_id = response['Count'] + 7000  # Add 7000 to start from 7000

    # Store the latest ID in the Flask application context for future use
    g.latest_id = latest_id

    return latest_id

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':

        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table('userdata')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:

            return render_template("home.html",name = name)
    return render_template("login.html")
@app.route('/home')
def home():
    return render_template('home.html')





if __name__ == "__main__":

    app.run(debug=True)
