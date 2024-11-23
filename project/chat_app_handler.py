import boto3
import json

from app1 import get_query_response, get_similar_documents, get_vector_store
from pdf_processor import create_chunks_from_pdf

def send_message(connection_id, endpoint_url, message):
    session = boto3.Session()
    client = session.client("apigatewaymanagementapi", endpoint_url=endpoint_url)
    response = client.post_to_connection(
    Data=json.dumps(message),
    ConnectionId=connection_id
)

def prompt_handler(event, context):
    try:
        if "headers" not in event:
            connection_id = event['requestContext']["connectionId"]
            endpoint_url = f"https://{event['requestContext']['apiId']}.execute-api.us-east-1.amazonaws.com/dev"
            event_body = json.loads(event["body"])
            query = event_body("query")
            vector_store =get_vector_store()
            docs = get_similar_documents(query, vector_store)
            response = get_query_response(query, docs)
            send_message(connection_id, endpoint_url, response)        
        return {
            "statusCode": 200
        }
    except Exception as e:
        print("Error in sending response", str(e))

def pdf_process_handler(event, context):
    print("PDF prcess lambda hit")
    print(event)
    create_chunks_from_pdf(pdf_path = None)

