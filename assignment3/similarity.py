from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from os import path
import glob

folder_path = 'assignment3/data/'
all_files = glob.iglob(path.join(folder_path, "*.csv"))

df_from_each_file = (pd.DataFrame(pd.read_csv(f)[['content', 'account_category', 'tweet_id']]) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df = concatenated_df[~concatenated_df.account_category.str.startswith("NonEnglish")]
#concatenated_df['content'] = concatenated_df['content'].str.findall('\w{2,}').str.join(' ')
concatenated_df['content'] = concatenated_df['content'].astype(str)

vec = TfidfVectorizer(stop_words="english", ngram_range=(1,3))
vec.fit(concatenated_df.content.values)
features = vec.transform(concatenated_df.content.values)
cosine_sim = cosine_similarity(features)
concatenated_df['cos_sim'] = cosine_sim

print("Writing file")
with open("similarity_results.csv", 'w') as analysis_file:
    for _, row in concatenated_df.iterrows():
        tweet_id = row['tweet_id']
        analysis_file.write(f"{tweet_id},{row['cos_sim']}\n")