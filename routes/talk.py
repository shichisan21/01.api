from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
import uuid

router = APIRouter()


class Item(BaseModel):
    id: str = str(uuid.uuid4())
    startDate: str
    endDate: str


def create_dynamodb_client():
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
    return dynamodb


def get_item(dynamodb, table_name, id):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            "Id": id
        }
    )
    return response.get("Item", None)


def put_item(dynamodb, table_name, item):
    table = dynamodb.Table(table_name)
    unique_id = str(uuid.uuid4())
    response = table.put_item(
        Item={"Id": unique_id, "startDate": item.startDate,
              "endDate": item.endDate}
    )
    return response


@router.get("/get_item/{id}")
def read_item(id: str):
    dynamodb = create_dynamodb_client()
    item = get_item(dynamodb, "talk-app-table", id)
    return item


@router.post("/put_item/")
def create_item(item: Item):
    dynamodb = create_dynamodb_client()
    response = put_item(dynamodb, "talk-app-table", item)
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise HTTPException(status_code=400, detail="Item could not be stored")
    return response
