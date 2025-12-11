import boto3
import json

table_name = "Emp_Master"
dynamo = boto3.resource("dynamodb").Table(table_name)


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


# ------------------ CREATE ------------------
def create(body):
    try:
        dynamo.put_item(Item=body)
        return response(200, {"message": f"Employee {body['Emp_Id']} created successfully"})
    except Exception as e:
        return response(500, {"error": str(e)})


# ------------------ READ ------------------
def read(emp_id):
    try:
        result = dynamo.get_item(Key={"Emp_Id": emp_id})
        if "Item" in result:
            return response(200, result["Item"])
        else:
            return response(404, {"message": f"Employee {emp_id} not found"})
    except Exception as e:
        return response(500, {"error": str(e)})


# ------------------ MAIN LAMBDA HANDLER ------------------
def lambda_handler(event, context):

    method = event.get("httpMethod", "")

    # ---------- POST ----------
    if method == "POST":
        body = event.get("body", "{}")

        try:
            body = json.loads(body)
        except:
            return response(400, {"error": "Invalid JSON body"})

        if "Emp_Id" not in body:
            return response(400, {"error": "Emp_Id is required"})

        return create(body)

    # ---------- GET ----------
    elif method == "GET":
        params = event.get("queryStringParameters", {})

        if not params or "Emp_Id" not in params:
            return response(400, {"error": "Emp_Id query parameter is required"})

        return read(params["Emp_Id"])

    else:
        return response(400, {"error": f"Unsupported method {method}"})


'''
import boto3
import json
 
# Define the DynamoDB table that Lambda will connect to
table_name = "Emp_Master"
 
# Create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(table_name)
 
def response(status, body):
    return {
        'statusCode': status,
        'body': json.dumps(body)
    }

# Define some functions to perform the CRUD operations
def create(body):
    try:
        response = dynamo.put_item(Item=body)
        if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return {
                'statuscode': 200,
                'body': json.dumps({'message': f"Employee {body['Emp_Id']} created successfully"})
            }
        else:
            return {
                'statuscode': 400,
                'body': json.dumps({'message': f"Employee {body['Emp_Id']} creation failed"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f"Error: {str(e)}"
            })
        }
 
def read(Emp_Id):
    try:
        response = dynamo.get_item(Key=Emp_Id)
       
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])  # converts dict to JSON string
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': f"Employee {Emp_Id} not found"
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f"Error: {str(e)}"
            })
        }
 
def lambda_handler(event, context):  
    method = event.get('httpMethod', {})
 
    if method == 'POST':
        body = event.get('body', '{}')
        try:
            body = json.loads(body)
        except Exception:
            return response(400, {"error": "Invalid JSON body"})
 
        if "Emp_Id" not in body:
            return response(400, {"error": "Emp_Id is required"})
 
        return create(body)
 
    elif method == 'GET':
        param = event.get('queryStringParameters', None)
        if not param.get('Emp_Id'):
            return response(400, {"error": "Emp_Id query parameter is required"})
        return read(param)
   
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': f"Unrecognized operation: '{method}'"
            })
        }
 
'''
