""" 
This file container all the helper functions.
"""

import pandas as pd
import re
from datetime import datetime, date, timedelta
import os


FILES_FOLDER = "D:/products/FORECAST_FINAL_PROJECT/P2P_ADJUSTED_OPS/ALL/FINAL_OPS"


# send only the seasons with avaiable forecasts to the dropdown
def seasons_available():

    # getting the latest file
    files = get_files_in_directory(FILES_FOLDER)
    latest_file = get_latest_file(files)
    # print("these are the files ", files)

    # print("this is the latest file ", latest_file)

    # reading the content of the files using pandas
    df = pd.read_excel(os.path.join(FILES_FOLDER, latest_file), nrows=1)

    # check availability of season
    colnames = list(df.columns)
    # season-month mapping
    season_month_mapping = {
        "SP": pd.date_range(start="02/01/2018", periods=3, freq="1M").strftime("%b"),
        "SU": pd.date_range(start="05/01/2018", periods=3, freq="1M").strftime("%b"),
        "FE": pd.date_range(start="07/01/2018", periods=4, freq="1M").strftime("%b"),
        "WI": pd.date_range(start="11/01/2018", periods=3, freq="1M").strftime("%b"),
    }

    # getting the unique years present in the output
    # print("getting the unique -yrs present in the o/p")
    unique_yrs = []
    for col in colnames:
        if len(col.split("-")) == 2:
            unique_yrs.append(col.split("-")[1])
    unique_yrs = list(set(unique_yrs))

    # getting the list of seasons
    seasons = season_month_mapping.keys()
    # list to capture the seasons with forecast available
    seasons_available = []
    for yr in unique_yrs:
        for season in seasons:
            if set([s + "-" + yr for s in season_month_mapping[season]]).issubset(
                set(colnames)
            ):
                seasons_available.append(season + "-" + yr)

    # print("these are the available seasons", seasons_available)

    # the available seasons are only sent to the dropdown
    return seasons_available, latest_file


# method to get list of latest files
def get_files_in_directory(directory):
    """return all the valid output forecast files

    Args:
        directory (_type_): this containes all the o/p files

    Returns:
        _type_: list of .xlsx forecast file paths
    """

    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            files.append(filename)
    return files


def get_latest_file(files):
    """gets the latest files based on dates"""

    ls_date = []
    if files:
        for file in files:
            date = file.split("_")[0]
            ls_date.append(datetime.strptime(date, "%b-%Y"))
    ls_date.sort(reverse=True)

    ls_sorted = []
    for date in ls_date:
        str_date = date.strftime("%b-%Y")
        for file in files:
            if str_date in file:
                ls_sorted.append(file)
                break
        break
    # getting the date prior to the given date
    return ls_sorted[-1]


def season_mapping(df, season_yr):
    """return season wise data"""

    colnames = list(df.columns)

    season_month_mapping = {
        "SP": pd.date_range(start="02/01/2018", periods=3, freq="1M").strftime("%b"),
        "SU": pd.date_range(start="05/01/2018", periods=3, freq="1M").strftime("%b"),
        "FE": pd.date_range(start="07/01/2018", periods=4, freq="1M").strftime("%b"),
        "WI": pd.date_range(start="11/01/2018", periods=3, freq="1M").strftime("%b"),
    }

    # season_yr = 'SP-2024'
    season_yr_ls = season_yr.split("-")
    season, yr = season_yr_ls[0], season_yr_ls[1]
    season_mon = season_month_mapping[season]

    ls_mon = []
    for mon in season_mon:
        month_yr = mon + "-" + yr
        r = re.compile(month_yr)
        mon_ls = list(filter(r.match, colnames))
        if len(mon_ls) != 0:
            ls_mon.append(mon_ls[0])

    if len(ls_mon) == len(season_mon):
        filtered_dataframe = df.filter(
            items=[
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
            ]
            + ls_mon
        )
    else:
        print("forecast not generated for the given period")
    return filtered_dataframe


def get_last_month(latest_file_name):

    file_month = latest_file_name.split("_")[0]
    current_month = datetime.strptime(file_month, "%b-%Y")
    last_month = current_month.replace(day=1) - timedelta(1)
    return last_month.strftime("%B %Y")
