import csv
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, Response, FileResponse
from fastapi.templating import Jinja2Templates
import os
import io
import sys
import openpyxl
from datetime import datetime

sys.path.append(os.path.abspath('C:/Users/Harleen kaur Bagga/AppData/Local/Programs/Python/Python310'))

app = FastAPI()
templates = Jinja2Templates(directory="templates")



# Folder path to fetch files from
FILES_FOLDER = "D:/products/FORECAST_FINAL_PROJECT/P2P_ADJUSTED_OPS/ALL/FINAL_OPS"


@app.get("/")
async def read_root():
    return FileResponse("templates/index.html")



def convert_to_csv(file_content: bytes) -> bytes:
    # Decode the byte stream as a string
    file_string = file_content.decode("utf-8")

    # Split the string into lines
    lines = file_string.splitlines()

    # Write each line to the CSV string using csv.writer
    csv_content = ""
    with io.StringIO() as csv_buffer:
        csv_writer = csv.writer(csv_buffer, quoting=csv.QUOTE_ALL, lineterminator='\n')
        for line in lines:
            row = line.split(",")
            csv_writer.writerow(row)
        csv_content = csv_buffer.getvalue()

    return csv_content.encode("utf-8")


@app.get("/download_csv")
def download_csv():
    # Read the example CSV file
    with open(f"D:/products/FORECAST_FINAL_PROJECT/P2P_ADJUSTED_OPS/ALL/ALL_STR_DEPT_ADJ_FCST.csv", "rb") as file_obj:
        file_content = file_obj.read()   
    
    # Convert the file content to CSV
    csv_content = convert_to_csv(file_content)
    
    # Create a streaming response to download the CSV
    def stream_response():
        yield csv_content


    return StreamingResponse(stream_response(), media_type="text/csv", headers=
                                   {"Content-Disposition": "attachment; filename=output.csv"
    })

@app.get("/download_xlsx")
def download_xlsx():
    
    #getting the latest file
    files = get_files_in_directory(FILES_FOLDER)
    latest_file = get_latest_file(files)
    print(latest_file)
    # Read the example CSV file
    with open(os.path.join(FILES_FOLDER, latest_file), "rb") as file_obj:
        file_content = file_obj.read()

    # Convert the file content to CSV
    xlsx_content = convert_to_xlsx(file_content)
    
    # Create a streaming response to download the CSV
    def stream_response():
        yield xlsx_content
    
    return StreamingResponse(stream_response(), media_type="xlsx", headers=
                                   {"Content-Disposition": f'attachment; filename="{latest_file}"' })
    
def convert_to_xlsx(file_content: bytes) -> bytes:
    # Load the byte stream as an Excel workbook using openpyxl
    workbook = openpyxl.load_workbook(io.BytesIO(file_content))
    
    # Create a new Excel file in memory
    output_buffer = io.BytesIO()    
    
    # Save the workbook to the output buffer
    workbook.save(output_buffer)
    
    print(workbook)
    
    # Get the contents of the output buffer as bytes
    xlsx_content = output_buffer.getvalue()

    return xlsx_content 

#method to get list of latest files
def get_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            files.append(filename)
    return files
 
def get_latest_file(files):
    ls_date = []
    if files:
        for file in files:
            date = file.split("_")[0]
            ls_date.append(datetime.strptime(date, '%b-%Y'))
    ls_date.sort(reverse= True)
    ls_sorted=[]
    for date in ls_date:
        str_date=date.strftime("%b-%Y")
        for file in files:
            if str_date in file:
                ls_sorted.append(file)
                break
        break
    return ls_sorted[-1]            
            
        





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
