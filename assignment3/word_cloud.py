import numpy as np
import pandas as pd
import glob
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
folder_path = 'assignment3/data/'
all_files = glob.iglob(path.join(folder_path, "*.csv"))

df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df = concatenated_df[~concatenated_df.account_category.str.startswith("NonEnglish")]
concatenated_df['content'] = concatenated_df['content'].str.findall('\w{2,}').str.join(' ')
# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["http", "https", "com", "co", "amp", "NowPlaying"])

text = " ".join(str(tweet) for tweet in concatenated_df.content)
# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()