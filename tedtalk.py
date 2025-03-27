# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import ast

# Load the datasets
ted_main_path = "ted_main.csv"
transcripts_path = "transcripts.csv"

ted_main_df = pd.read_csv(ted_main_path)
transcripts_df = pd.read_csv(transcripts_path)

# Convert film_date and published_date to datetime
ted_main_df['film_date'] = pd.to_datetime(ted_main_df['film_date'], unit='s')
ted_main_df['published_date'] = pd.to_datetime(ted_main_df['published_date'], unit='s')

# Basic data info and shape
print(ted_main_df.info())
print(ted_main_df.head())
print(transcripts_df.info())

# Merge transcripts with ted_main_df on URL
ted_df = pd.merge(ted_main_df, transcripts_df, on='url', how='left')

# 1. Most Viewed Talks
top_viewed = ted_df[['title', 'main_speaker', 'views']].sort_values(by='views', ascending=False).head(10)
print(top_viewed)

# 2. Most Commented Talks
top_commented = ted_df[['title', 'main_speaker', 'comments']].sort_values(by='comments', ascending=False).head(10)
print(top_commented)

# 3. Top Speaker Occupations
top_occupations = ted_df['speaker_occupation'].value_counts().head(10)
print(top_occupations)

# 4. Talk Duration Analysis
ted_df['duration_minutes'] = ted_df['duration'] / 60
plt.figure(figsize=(10, 6))
sns.histplot(ted_df['duration_minutes'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Talk Durations')
plt.xlabel('Duration (minutes)')
plt.ylabel('Count')
plt.show()

# 5. Top-rated Talks (Based on Inspiring, Funny, etc.)
def get_highest_rating(row):
    ratings_list = ast.literal_eval(row)
    top_rating = max(ratings_list, key=lambda x: x['count'])
    return top_rating['name']

# Extract top rating for each talk
ted_df['top_rating'] = ted_df['ratings'].apply(get_highest_rating)
top_rated_talks = ted_df['top_rating'].value_counts().head(10)
print(top_rated_talks)

# 6. Analyze Trends Over Time
ted_df['year'] = ted_df['film_date'].dt.year
yearly_trends = ted_df.groupby('year').size()
yearly_trends.plot(kind='line', figsize=(12, 6), title='Number of TED Talks Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Talks')
plt.show()

# 7. Word Cloud of Most Frequent Words in Transcripts
all_transcripts = ' '.join(transcripts_df['transcript'].dropna())
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=600).generate(all_transcripts)
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in TED Talks Transcripts')
plt.show()

cd "C:\path\to\your\project\folder"


# Export Top Results
top_viewed.to_csv('top_viewed_talks.csv', index=False)
top_commented.to_csv('top_commented_talks.csv', index=False)
top_occupations.to_csv('top_speaker_occupations.csv', header=['count'])

echo "# tedtalk.py" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/guptapiyush7067/tedtalk.py.git
git push -u origin main