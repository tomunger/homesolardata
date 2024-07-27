import pandas as pd

import sdlib



# Load configuration
source_list, target = sdlib.load_yaml_config("local-database.yaml")

# Load and merge the source data sets
#
df_list: list[pd.DataFrame] = []
for source in source_list:
    df = sdlib.load_database(source)
    df.info()
    df_list.append(df)

total_df = pd.concat(df_list)



# Resample to 1 minute.
# '1T' is 1 minute:  https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
#                    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
rs =  total_df.resample('1T', on='datetime')
resample_df = rs.mean() # .interpolate(method='linear', axis=0)
resample_df = resample_df.dropna()

# Save
resample_df.info()
# 719940 rows
sdlib.save_database(target, resample_df)

print ("done")