from fastapi import APIRouter
from datetime import datetime
import pytz

router = APIRouter()


@router.get("/current_time")
def get_current_time():
    local_time = datetime.now().astimezone(pytz.timezone('Asia/Tokyo'))  # 例として日本時間
    utc_time = datetime.utcnow().replace(tzinfo=pytz.UTC)

    return {
        "local_time": local_time.isoformat(),
        "utc_time": utc_time.isoformat()
    }
