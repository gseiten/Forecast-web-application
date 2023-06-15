import csv
from fastapi import FastAPI, Request, Form
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
import json

from helpers import (
    seasons_available,
    get_files_in_directory,
    get_latest_file,
    season_mapping,
    get_last_month,
)

from loguru import logger
from config import output_path

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Folder path to fetch files from
FILES_FOLDER = output_path


@app.get("/")
async def home(request: Request):

    seasons, latest_file = seasons_available()
    last_month = get_last_month(latest_file)
    return templates.TemplateResponse(
        "index.html", {"request": request, "season": seasons, "last_month": last_month}
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

    seasons, _ = seasons_available()

    form_data = await request.form()
    selected_season = form_data["selected_season"]
    print(selected_season)

    # return json.dumps(season_data)
    # return Response(content=season_data, media_type="application/json")

    # return templates.TemplateResponse(
    #     "forecast_preview.html", {"request": request, "season_data": season_data}
    # )

    # getting the latest file
    files = get_files_in_directory(FILES_FOLDER)
    latest_file = get_latest_file(files)

    # reading the content of the files using pandas
    file_df = pd.read_excel(os.path.join(FILES_FOLDER, latest_file))

    # data with filtered out season
    season_df = season_mapping(file_df, selected_season)
    data_list = season_df.to_dict(orient="records")
    data_list = data_list[0:5000]

    season_data = {
        "headers": list(season_df.columns),
        "rows": data_list,
    }

    return templates.TemplateResponse(
        "forecast_preview.html",
        {
            "request": request,
            "season_data": season_data,
            "selected_season": selected_season,
            "seasons": seasons,
        },
    )


@app.get("/fetch_data")
async def redirect_home():
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9003)
