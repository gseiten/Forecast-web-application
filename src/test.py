import pandas as pd
import re


file_path= "D:/products/FORECAST_FINAL_PROJECT/P2P_ADJUSTED_OPS/ALL/ALL_STR_DEPT_ADJ_FCST.xlsx"


def season_mapping(forecast_tbl, season_yr):
    colnames= list(df.columns)
    season_month_mapping={
        'SP':pd.date_range(start='02/01/2018', periods=3, freq='1M').strftime("%b"),
        'SU':pd.date_range(start='05/01/2018', periods=3, freq='1M').strftime("%b"),
        'FE':pd.date_range(start='07/01/2018', periods=4, freq='1M').strftime("%b"),
        'WI':pd.date_range(start='11/01/2018', periods=4, freq='1M').strftime("%b")
        }


    #season_yr = 'SP-2024'
    season_yr_ls= season_yr.split("-")
    season, yr= season_yr_ls[0], season_yr_ls[1]
    season_mon= season_month_mapping[season]

    ls_mon=[]   
    for mon in season_mon:
            month_yr = mon+"-"+yr
            r = re.compile(month_yr)
            mon_ls =  list(filter(r.match, colnames))
            if len(mon_ls)!=0:
                ls_mon.append(mon_ls[0])

    if len(ls_mon)==len(season_mon):
        filtered_dataframe = df.filter(items=['store', 'site_code', 'tier', 'region', 'zone', 'division', 'section', 'season', 'dept_name', 'dept_code']+ls_mon)
    else:
        print("forecast not generated for the given period")
    return filtered_dataframe

df = pd.read_excel(file_path)
season_yr= "SP-2024"
#seasonal_df= season_mapping(df, season_yr)
#print(seasonal_df)

#check availability of season
colnames= list(df.columns)
season_month_mapping={
        'SP':pd.date_range(start='02/01/2018', periods=3, freq='1M').strftime("%b"),
        'SU':pd.date_range(start='05/01/2018', periods=3, freq='1M').strftime("%b"),
        'FE':pd.date_range(start='07/01/2018', periods=4, freq='1M').strftime("%b"),
        'WI':pd.date_range(start='11/01/2018', periods=4, freq='1M').strftime("%b")
        }

print("split completed")
#season_yr = 'SP-2024'
season_yr_ls= season_yr.split("-")

print("this is season year list", season_yr_ls)
#getting the unique years present in the output

print("these are the unique years")
unique_yrs= []
for col in colnames:
    if(len(col.split("-"))==2):
        unique_yrs.append(col.split("-")[1])
unique_yrs= list(set(unique_yrs))

print(unique_yrs)

#getting the list of seasons 
seasons = season_month_mapping.keys()

print("these are the list of seasons")
#list to capture the seasons with forecast available
season_avai = []

for yr in unique_yrs:
    for season in seasons:
        if set([s + "-" + yr  for s in season_month_mapping[season]]).issubset(set(colnames)):
            season_avai.append(season+"-"+yr)

print("these are the available seasons",season_avai)        








       
         
              
     
     
    
    



