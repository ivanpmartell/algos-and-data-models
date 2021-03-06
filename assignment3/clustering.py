from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
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

print("Fitting tfidf")
vec = TfidfVectorizer(stop_words="english", ngram_range=(1,3))
vec.fit(concatenated_df.content.values)
features = vec.transform(concatenated_df.content.values)

print("Doing KMeans")
#For each type 'RightTroll' 'Fearmonger' 'Unknown' 'NewsFeed' 'LeftTroll' 'HashtagGamer' 'Commercial'
clust = KMeans(init='k-means++', n_clusters=7, n_init=10)
clust.fit(features)

print("Getting clusters into pandas")
yhat = clust.predict(features)
concatenated_df['cluster_lbl'] = clust.labels_

print("Writing file")
with open("clustering_results.csv", 'w') as analysis_file:
    for _, row in concatenated_df.iterrows():
        tweet_id = row['tweet_id']
        analysis_file.write(f"{tweet_id},{row['cluster_lbl']}\n")