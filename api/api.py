import flask
from flask import request, jsonify
import boto3
import json
import os

app = flask.Flask(__name__)

s3 = boto3.client('s3',
                  aws_access_key_id= os.environ['ACCESS_KEY'], 
                  aws_secret_access_key=os.environ['SECRET_ACCESS_KEY'], 
                  region_name='us-east-1')


@app.route('/', methods=['GET'])
def home():
    return '''<h1>iFood Data Engineer Test</h1>
<p>A API developed for a restaurant front end.</p>'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/toprestaurants', methods=['GET'])
def api_top():

    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    query = f"SELECT s.customer_id, s.merchant_id, s.number_of_orders, s.rank FROM s3object s WHERE s.customer_id = '{id}'"


    r = s3.select_object_content(
        Bucket='ifood-de-test-arb',
        Key='top_rest_by_customer_no_partition.json/part-00000-tid-703590415988688684-acccc201-9bb2-45f7-9ffb-c50f85c7fc7e-85-1-c000.json',
        ExpressionType='SQL',
        Expression=query,
        InputSerialization = {'JSON': {"Type": "Lines"}},
        OutputSerialization = {'JSON': {}},
    )

    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            res = records
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']

    try:
        res = '[' + res.replace('\n', ',')[:-1] + ']'
    except:
        res = res

    return jsonify(json.loads(res))

@app.route('/api/v1/resources/dailyorders', methods=['GET'])
def api_daily():
    query_parameters = request.args

    query_parameters = request.args

    if 'date' in request.args:
        date = request.args['date']
    else:
        return "Error: No date field provided. Please specify a date."

    if 'state' in request.args:
        state = request.args['state']
        query = f"SELECT SUM(s.number_of_orders) as number_of_orders FROM s3object s WHERE s.delivery_address_state = '{state}' and s.date_partition_local = '{date}'"
    elif 'city' in request.args:
        city = request.args['city']
        query = f"SELECT SUM(s.number_of_orders) as number_of_orders FROM s3object s WHERE s.delivery_address_city = '{city}' and s.date_partition_local = '{date}'"
    else:
        return "Error: No city or state field provided. Please specify one."


    r = s3.select_object_content(
        Bucket='ifood-de-test-arb',
        Key='top_orders_city_state.json/part-00000-tid-6029214069021578370-4074be7b-9194-425f-880d-ae49f75f5939-97-1-c000.json',
        ExpressionType='SQL',
        Expression=query,
        InputSerialization = {'JSON': {"Type": "Lines"}},
        OutputSerialization = {'JSON': {}},
    )

    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            res = records
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']

    try:
        res = '[' + res.replace('\n', ',')[:-1] + ']'
    except:
        res = res

    return jsonify(json.loads(res))

app.run(debug=False, host='0.0.0.0')