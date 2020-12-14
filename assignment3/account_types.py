import pandas as pd
from os import path
import glob

folder_path = 'assignment3/data/'
all_files = glob.iglob(path.join(folder_path, "*.csv"))

df_from_each_file = (pd.DataFrame(pd.read_csv(f)[['account_category']]) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

print(concatenated_df.account_category.unique())