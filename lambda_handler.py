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
 
 
# ------------------ UPDATE ------------------
def update(emp_id, body):
    try:
        update_expr = "SET " + ", ".join(f"{k} = :{k}" for k in body.keys())
        expr_values = {f":{k}": v for k, v in body.items()}
 
        dynamo.update_item(
            Key={"Emp_Id": emp_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values
        )
 
        return response(200, {"message": f"Employee {emp_id} updated successfully"})
    except Exception as e:
        return response(500, {"error": str(e)})
 
 
# ------------------ DELETE ------------------
def delete(emp_id):
    try:
        dynamo.delete_item(Key={"Emp_Id": emp_id})
        return response(200, {"message": f"Employee {emp_id} deleted"})
    except Exception as e:
        return response(500, {"error": str(e)})
 
 
# ------------------ MAIN HANDLER ------------------
def lambda_handler(event, context):
 
    method = event.get("httpMethod", "")
    params = event.get("queryStringParameters", {}) or {}
 
    # ---------- POST (Create) ----------
    if method == "POST":
        body = json.loads(event.get("body", "{}"))
        if "Emp_Id" not in body:
            return response(400, {"error": "Emp_Id is required"})
        return create(body)
 
    # ---------- GET (Read) ----------
    elif method == "GET":
        if "Emp_Id" not in params:
            return response(400, {"error": "Emp_Id query parameter is required"})
        return read(params["Emp_Id"])
 
    # ---------- PUT (Update) ----------
    elif method == "PUT":
        if "Emp_Id" not in params:
            return response(400, {"error": "Emp_Id is required"})
        body = json.loads(event.get("body", "{}"))
        return update(params["Emp_Id"], body)
 
    # ---------- DELETE ----------
    elif method == "DELETE":
        if "Emp_Id" not in params:
            return response(400, {"error": "Emp_Id is required"})
        return delete(params["Emp_Id"])
 
    else:
        return response(400, {"error": f"Unsupported method {method}"})
 
Microsoft Windows [Version 10.0.26200.7171]

(c) Microsoft Corporation. All rights reserved.
 
C:\Users\SaiKrishnaAkula>curl -x POST ^

More?   -H "Content-Type: application/json" ^

More?   -d "{\"Emp_Id\":\"E102\",\"First_Name\":\"Sumit\",\"Last_Name\":\"Dhar\",\"Date_Of_Joining\":\"2023-10-02\"}" ^

More? https://30ghddnfxa.execute-api.ap-south-1.amazonaws.com/Test

curl: (5) Could not resolve proxy: POST
 
C:\Users\SaiKrishnaAkula>curl -x POST ^

More? ^X
 
C:\Users\SaiKrishnaAkula>https://30ghddnfxa.execute-api.ap-south-1.amazonaws.com/Test/APIgateway ^

More? -H "Content-Type: application/json" ^

More? -d "{\"Emp_Id\":\"E102\",\"First_Name\":\"Sumit\",\"Last_Name\":\"Dhar\",\"Date_Of_Joining\":\"2023-10-02\"}"

'https:' is not recognized as an internal or external command,

operable program or batch file.
 
C:\Users\SaiKrishnaAkula>curl https://30ghddnfxa.execute-api.ap-south-1.amazonaws.com/Test/APIgateway ^

More? -H "Content-Type: application/json" ^

More?   -d "{\"Emp_Id\":\"E102\",\"First_Name\":\"Sumit\",\"Last_Name\":\"Dhar\",\"Date_Of_Joining\":\"2023-10-02\"}"

{"message": "Employee E102 created successfully"}

C:\Users\SaiKrishnaAkula>curl https://30ghddnfxa.execute-api.ap-south-1.amazonaws.com/Test/APIgateway ^

More? -H "Content-Type: application/json" ^

More?
 
C:\Users\SaiKrishnaAkula>curl https://30ghddnfxa.execute-api.ap-south-1.amazonaws.com/Test/APIgateway?Emp_Id=E102

{"Last_Name": "Dhar", "Emp_Id": "E102", "First_Name": "Sumit", "Date_Of_Joining": "2023-10-02"}

C:\Users\SaiKrishnaAkula>
 
name: CI/CD to Lambda using ECR Image
 
on:

  push:

    branches:

      - dev
 
jobs:

  deploy:

    runs-on: ubuntu-latest
 
    env:

      AWS_REGION: ap-south-1

      ECR_REPOSITORY: lambda-ecr-repo

      LAMBDA_FUNCTION_NAME: LambdaFunctionOverHttps
 
    steps:

      - name: Checkout repository

        uses: actions/checkout@v3
 
      - name: Configure AWS credentials

        uses: aws-actions/configure-aws-credentials@v2

        with:

          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}

          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

          aws-region: ${{ env.AWS_REGION }}
 
      - name: Login to Amazon ECR

        id: login-ecr

        uses: aws-actions/amazon-ecr-login@v1
 
      - name: Build Docker image

        run: |

          docker build -t $ECR_REPOSITORY:latest .
 
      - name: Tag Docker image

        run: |

          docker tag $ECR_REPOSITORY:latest ${{ steps.login-ecr.outputs.registry }}/${ECR_REPOSITORY}:latest
 
      - name: Push Docker image to ECR

        run: |

          docker push ${{ steps.login-ecr.outputs.registry }}/${ECR_REPOSITORY}:latest
 
      - name: Update Lambda with ECR Image

        run: |

          IMAGE_URI=${{ steps.login-ecr.outputs.registry }}/${ECR_REPOSITORY}:latest

          aws lambda update-function-code \

            --function-name ${{ env.LAMBDA_FUNCTION_NAME }} \

            --image-uri $IMAGE_URI

 FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ./
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY lambda_handler.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_handler.lambda_handler" ]



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
