# -*- coding: utf-8 -*-
"""
Created on Tue Jue 6 12:36:03 2023

@author: Sumana Chittamuri
"""

import boto3
# Get the service resource.


dynamodb = boto3.resource('dynamodb',
                   aws_access_key_id= "ASIA2X5HZ7YKYJEUZZQI",
        aws_secret_access_key= "J4oPxXr10+nmj3pFK2yH1TJah1+0zGNtm33QSmJk",
        aws_session_token= "IQoJb3JpZ2luX2VjEAsaCXVzLWVhc3QtMSJGMEQCICfYVHjWdC4oRvvtRaB0TmEkxGaV9dlvJplzj6i6UNKTAiBz96d3EICD0XrUfy1OXDz6Jq97bAEf8/mJsqMbe0Z0ySrTAQhUEAAaDDczODU0OTQzMTgyOSIMso/yoGjL/3L17M0eKrABwL5arHIbZT5XqQ8ZZGzktCBH7waa1IgQIYenx6z7YIbWEcRrvpsU3E1ywK5dKtVUQ9ogTSheSbbgCQRmGohtD2J4FHrb5iqEHFFZ8UcvSi4TTCRicXtU97HFMD1zhcAzhYBjUBqw2oubKqTnvma/Ykq+pk/niy7KDHcr3vZKIS5VzzxfZR4uq9N9H8yufPY2uQ5X6FUi17cSgsJxol71wrRFp5Na7NyOqgGa1MGCPx8w3uL/owY6mQGn6uZTiKxSLbx77VZ7cflr2LNY7TbwTxm4idlq7YoZFHJQXMQWbjK5WuoyIQ7qhVGCxsHlkf+1xRekut7t5WGv89fmURw7GBeZ50WQmFJ5mErS2VZV0VbfuJ7nzJuCVtnpIeL5HwOmR9VZJ3xBD2ZY9qjdZVTm2Yn5YBOQOm2Fv/hkciRklZPyiQOOaMTgdRTKe7cGcloLkn0="
        )

#dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='userdata',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
         
    ],
    AttributeDefinitions=[
             {
            'AttributeName': 'email',
            'AttributeType': 'S'
        } 
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='userdata')

# Print out some data about the table.
print(table.item_count)




 