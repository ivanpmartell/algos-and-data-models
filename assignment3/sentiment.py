import nltk
import pandas as pd
import glob
from os import path
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

folder_path = 'assignment3/data/'
all_files = glob.iglob(path.join(folder_path, "*.csv"))

df_from_each_file = (pd.DataFrame(pd.read_csv(f)[['content', 'account_category', 'tweet_id']]) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df = concatenated_df[~concatenated_df.account_category.str.startswith("NonEnglish")]
concatenated_df['content'] = concatenated_df['content'].str.findall('\w{2,}').str.join(' ')

with open("sentiment_results.csv", 'w') as analysis_file:
    for _, row in concatenated_df.iterrows():
        content = row['content']
        tweet_id = row['tweet_id']
        polarity = sid.polarity_scores(str(content))
        analysis_file.write(f"{tweet_id},{polarity['compound']},{polarity['neg']},{polarity['pos']},{polarity['neu']}\n")
