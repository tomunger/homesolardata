import pandas as pd

import sdlib



   

source_list, target = sdlib.load_yaml_config("local-database.yaml")

df_list: list[pd.DataFrame] = []
for source in source_list:
    df = sdlib.load_database(source)
    df.info()
    df_list.append(df)

total_df = pd.concat(df_list)
    # if total_df is None:
    #     total_df = df
    # else:
    #     total_df.append(df)



resample_df =  total_df.resample('1T', on='datetime').mean().interpolate(method='linear', axis=0)

resample_df.info()
# 719940 rows
sdlib.save_database(target, resample_df)

print ("done")