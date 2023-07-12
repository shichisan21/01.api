from fastapi import FastAPI, UploadFile, File, APIRouter
router = APIRouter()


@router.post("/upload-csv/")
async def process_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded_content = contents.decode("utf-8")
    csv_data = csv.reader(decoded_content.splitlines(), delimiter=",")

    data_array = []

    for row in csv_data:
        data_array.append(row)

    print(data_array)

    return {"message": "CSV file received and processed successfully",  "data": data_array}
