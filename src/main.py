import csv
from fastapi import FastAPI, Request
from fastapi.responses import (
    StreamingResponse,
    HTMLResponse,
    Response,
    FileResponse,
    JSONResponse,
    RedirectResponse,
)
from fastapi.templating import Jinja2Templates
import os
import io
import sys
from datetime import datetime
import pandas as pd
import re

from helpers import (
    seasons_available,
    get_files_in_directory,
    get_latest_file,
    season_mapping,
)

from loguru import logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Folder path to fetch files from
FILES_FOLDER = "D:/products/FORECAST_FINAL_PROJECT/P2P_ADJUSTED_OPS/ALL/FINAL_OPS"


@app.get("/")
async def home(request: Request):

    seasons = seasons_available()
    return templates.TemplateResponse(
        "index.html", {"request": request, "season": seasons}
    )


@app.get("/download_xlsx")
async def download_xlsx(request: Request, season: str):

    # getting the latest file
    files = get_files_in_directory(FILES_FOLDER)
    latest_file = get_latest_file(files)

    # reading the content of the files using pandas
    file_df = pd.read_excel(os.path.join(FILES_FOLDER, latest_file))

    # data with filtered out season
    season_df = season_mapping(file_df, season)

    # creating a BytesIO buffer
    file_df_bytes = io.BytesIO()
    # write to BytesIO buffer
    season_df.to_excel(file_df_bytes)
    file_df_bytes.seek(0)

    file_name = season + "_" + "demand_forecast" + ".xlsx"

    # Create a streaming response to download the Excel
    def stream_response():
        yield file_df_bytes.getvalue()

    return StreamingResponse(
        stream_response(),
        media_type="xlsx",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@app.post("/fetch_data")
async def fetch_data(request: Request):

    season_data = {
        "headers": [
            "store",
            "site_code",
            "tier",
            "region",
            "zone",
            "division",
            "section",
            "season",
            "dept_name",
            "dept_code",
            "May-2023",
            "Jun-2023",
            "Jul-2023",
        ],
        "rows": [
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Western",
                "section": "Western Lower",
                "season": "SUMMER",
                "dept_name": "Capri [L]",
                "dept_code": 107,
                "May-2023": 14315.25,
                "Jun-2023": 22264.95,
                "Jul-2023": 16669.65,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Western",
                "section": "Western Lower",
                "season": "SUMMER",
                "dept_name": "Shorts[L]",
                "dept_code": 155,
                "May-2023": 12971.4194602394,
                "Jun-2023": 14212.5,
                "Jul-2023": 8427.5,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Western",
                "section": "Western Upper",
                "season": "BASIC",
                "dept_name": "Shirt[L]",
                "dept_code": 57,
                "May-2023": 25945.0134121673,
                "Jun-2023": 26197.3993216597,
                "Jul-2023": 26046.3292847851,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Men",
                "section": "Mens Sports Wear",
                "season": "SUMMER",
                "dept_name": "Shorts[M]",
                "dept_code": 67,
                "May-2023": 201105.871561938,
                "Jun-2023": 199539.6,
                "Jul-2023": 155465.140809746,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Girls",
                "section": "Girls Toddler",
                "season": "AUTUMN",
                "dept_name": "Casual Set FS[GT]",
                "dept_code": 2574,
                "May-2023": 700.0,
                "Jun-2023": 931.0,
                "Jul-2023": 1110.4,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Ethnic",
                "section": "Ethnic Upper",
                "season": "SUMMER",
                "dept_name": "Kurti[L]",
                "dept_code": 5517,
                "May-2023": 4837.5,
                "Jun-2023": 3524.1,
                "Jul-2023": 4473.15,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Western",
                "section": "Western Upper",
                "season": "AUTUMN",
                "dept_name": "Top FS[L]",
                "dept_code": 2473,
                "May-2023": 5161.6,
                "Jun-2023": 8057.7,
                "Jul-2023": 56953.5891666668,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Boys",
                "section": "Boys Senior",
                "season": "BASIC",
                "dept_name": "Shirt FS [BS]",
                "dept_code": 5669,
                "May-2023": 280.01,
                "Jun-2023": 1015.0,
                "Jul-2023": 623.128855645707,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Girls",
                "section": "Girls Senior",
                "season": "WINTER",
                "dept_name": "Sweater[GS]",
                "dept_code": 442,
                "May-2023": 0.0,
                "Jun-2023": 0.0,
                "Jul-2023": 0.0,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Ethnic",
                "section": "Saree",
                "season": "BASIC",
                "dept_name": "Synthetic Print[L]",
                "dept_code": 4488,
                "May-2023": 34851.8,
                "Jun-2023": 4237.5,
                "Jul-2023": 13665.7,
            },
            {
                "store": "arrah",
                "site_code": "46",
                "tier": "iii",
                "region": "bihar1",
                "zone": "bihar",
                "division": "Women Ethnic",
                "section": "Saree",
                "season": "BASIC",
                "dept_name": "Blouse[L]",
                "dept_code": 5599,
                "May-2023": 15754.0,
                "Jun-2023": 10449.0,
                "Jul-2023": 7899.0,
            },
        ],
    }

    return Response(content=season_data, media_type="application/json")

    return templates.TemplateResponse(
        "index.html", {"request": request, "season_data": season_data}
    )

    # getting the latest file
    files = get_files_in_directory(FILES_FOLDER)
    latest_file = get_latest_file(files)

    # reading the content of the files using pandas
    file_df = pd.read_excel(os.path.join(FILES_FOLDER, latest_file))

    # data with filtered out season
    season_df = season_mapping(file_df, "SU-2023")

    season_data = {
        "headers": list(season_df.columns),
        "rows": season_df.to_dict(orient="records"),
    }

    return templates.TemplateResponse(
        "index.html", {"request": request, "season_data": season_data}
    )


@app.get("/fetch_data")
async def redirect_home():
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
