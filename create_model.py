import boto3
import json

sm_client = boto3.client(service_name='sagemaker')

def create_model():
    role_arn = "arn:aws:iam::637423451884:role/admin"
    image = "637423451884.dkr.ecr.us-east-1.amazonaws.com/example-model:latest"
    create_model_response = sm_client.create_model(
        ModelName="example-model",
        ExecutionRoleArn=role_arn,
        Containers=[{"Image": image}],
    )
    print(create_model_response)

def create_endpoint_configuration():
    create_endpoint_config_response = sm_client.create_endpoint_config(
        EndpointConfigName="example-endpoint-config",
        ProductionVariants=[
            {
                "ModelName": "example-model",
                "VariantName": "example-1",
                "ServerlessConfig": {
                    "MemorySizeInMB": 2048,
                    "MaxConcurrency": 1,
                },
            }
        ],
    )
    print(create_endpoint_config_response)

def create_endpoint():
    create_endpoint_response = sm_client.create_endpoint(
        EndpointName="example-endpoint",
        EndpointConfigName="example-endpoint-config",
    )
    print("Endpoint Arn: " + create_endpoint_response["EndpointArn"])
    resp = sm_client.describe_endpoint(EndpointName="example-endpoint")
    print("Endpoint Status: " + resp["EndpointStatus"])
    print("Waiting for {} endpoint to be in service".format("example-endpoint"))
    waiter = sm_client.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName="example-endpoint")

runtime_sm_client = boto3.client(service_name="sagemaker-runtime")

def invoke_endpoint():
    content_type = "application/json"
    request_body = {}
    payload = json.dumps(request_body)
    response = runtime_sm_client.invoke_endpoint(
        EndpointName="example-endpoint",
        ContentType=content_type,
        Body=payload,
    )
    result = json.loads(response["Body"].read().decode())
    print(result)

def main():
    create_endpoint_configuration()
    create_endpoint()
    invoke_endpoint()

if __name__ == '__main__':
    main()