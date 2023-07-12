from fastapi import APIRouter
import boto3

router = APIRouter()


def create_dynamodb_client():
    dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
    return dynamodb


@router.get("/talk")
def Talk():
    return {"Hello": "World"}
