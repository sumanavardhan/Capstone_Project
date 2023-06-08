# -*- coding: utf-8 -*-
"""
Created on Tue Jue 6 16:39:56 2023

@author: Sumana Chittamuri
"""

from flask import Flask, render_template, request

import boto3

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id="ASIA2X5HZ7YK5DA7JYTR",
        aws_secret_access_key=  "BPv0+uiZ5BlEEJt6jXQKZ19BiZEJcTZSXzQ6qb+/",
        aws_session_token= "IQoJb3JpZ2luX2VjEBoaCXVzLWVhc3QtMSJHMEUCIQDAxSntZsTlLy3sBS3WxNp1ZGMwr5ZAaK99mlXkiu9jVgIgXxdp5kc45GtsNk8uJBzIIo5nXs8tVrUqrcEkQ87sAZIq0wEIYxAAGgw3Mzg1NDk0MzE4MjkiDLocx7QpamP26QO+kyqwAbr0hX/7NcILgIxofNkJ70pJPC9hoAEkeKvfwSSrWwtiTfBjQR8AOFsitV6lmh2jqPiy3T4WYc399xJACYMNi6T24q31Dk4yttQMOGhj2HDWiRWpb2vzJyuRASiNdAYHEqeHQSbxy2pAxQyyl4ljzDzNQbtfk5mXM/LEraleEThBukEfCurM04OR5AYIOQFcgofCUc7rOmzSuu9yScA3O4V0GPTnntTtShZhHTij86r9MJj6gqQGOpgB33CvpZAqfTK2OnDxvGQWBVHO6dOPoaOy4apa7zI0aW1jqmqyGTnh3Aj/xmhD8/jvofu+Eks/FaZI8t2WBVdX83GuVucq8oLAwBEwn9v29UEx+LnmNcde9cDDZbY3Mvgx6UHHOzxYyVFILcl0TcJCpBZ1l3NQTLmxf/93qgqfzkPF03w5Uetc8yt4txzdtwHQG6RHifbWBlg="
      )

dynamodbEmployee = boto3.resource('dynamodb',
                    aws_access_key_id="AKIAQENB5424S2QCDW2X",
                    aws_secret_access_key=  "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",
                    aws_session_token= "IQoJb3JpZ2luX2VjEDEaCXVzLWVhc3QtMSJHMEUCIQCs4AI8odKRGPwCOcnimc9dLMi6I0q0lHCIlMAydfD4PQIgFuWvzL8iUQFU7GKUoByHbEQmaau82Z0S8aZhMPndRKUq6wEIeRAAGgwwMDk0NjY0MDY1ODUiDJBEw+y3jS10zVuIAyrIAarmq4MrehonakHB+1KvF2byYJunqyaM1Ru9/GSwjycPBG15S53l9egHzFLE/HdT8r50018we9vu1eFy1f2nq/b/YQ84DzFYcnuCtRpilskKL64nU9OJIJ5cy8yG0798SNeEF/o3JbHbzqciSilJ10cfDEW7LEpBPRsytRNftPJDygX/yACqxYf5yB+WNNsSent0v04feLP0jvVvMyFkNOh6FY+ULH3fZpI6LF05hr2lFj48M7jqf7lO/1uat84BnQO8fiTp77xyMNv5h6QGOpgBK81SOehgcGDkvM9TjCCC74sC8Ecb8R7NNoBl7/t5MN0uD10L4GhOGl5dVQohPU70I/ootnCS2q/4kVWej9AT8GkU6S+7/okwKnoc2nZmdiV6XCRlc9lB1O0gdiXRMLP4AA8aETyt9Rvr/HvgTnOCHAbwFinvRcrS00wZWUyWGK3NRPZEvDoVeN/fGE+Wk21NQV8ULvzkOeU="
                    )

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['post'])
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

@app.route('/submission', methods=['post'])
def submission():
    if request.method == 'POST':
        
        age = request.form['age']
        gender = request.form['gender']
        education_level = request.form['education_level']
        job_title = request.form['job_title']
        years_of_experience = request.form['years_of_experience']
        salary = request.form['salary']
        
        table2 = dynamodbEmployee.Table('Salary')
        
        table2.put_item(
            Item={
                'age': age,
                'gender': gender,
                'education_level': education_level,
                'job_title': job_title,
                'years_of_experience': years_of_experience,
                'salary': salary
            }
        )
        
        return "Form submitted successfully!"
    
    return render_template('index.html')

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

