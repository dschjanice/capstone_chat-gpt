
# pip install google-play-scraper

import csv
from google_play_scraper import reviews_all, Sort

# Retrieve reviews for a specific app using the google_play_scraper library
result = reviews_all(
    'com.openai.chatgpt',  # App package name or ID
    sleep_milliseconds=0,  # Time to sleep between requests (0 by default)
    lang='en',  # Language for reviews
    # Country for reviews (Not applicable to English-speaking countries)
    country='gb',
    sort=Sort.NEWEST,  # Sort reviews by newest (default)
)

# Define the column names for the CSV file
fieldnames = ['reviewId', 'userName', 'content', 'score',
              'thumbsUpCount', 'reviewCreatedVersion', 'at', 'replyContent', 'repliedAt', 'appVersion']

# Create a CSV file and write the data
with open('USA_rew.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row with column names
    writer.writeheader()

    # Write data from each review dictionary, omitting any extra fields
    for review in result:
        filtered_review = {key: review[key]
                           for key in fieldnames if key in review}
        writer.writerow(filtered_review)
