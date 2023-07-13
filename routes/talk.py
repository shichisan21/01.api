from fastapi import APIRouter
import boto3

router = APIRouter()


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


@router.get("/get_item/{id}")
def read_item(id: int):
    dynamodb = create_dynamodb_client()
    item = get_item(dynamodb, "talk-app-table", id)
    return item
