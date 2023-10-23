import csv
from google_play_scraper import Sort, reviews_all
from google_play_scraper import Sort, reviews

from google_play_scraper import Sort, reviews_all

result = reviews_all(
    'com.openai.chatgpt',
    sleep_milliseconds=0,  # defaults to 0
    lang='en',  # defaults to 'en'
    country='uk',  # defaults to 'us'
    sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
    # filter_score_with=5 # defaults to None(means all score)
)


# Определите названия колонок для CSV
fieldnames = ['reviewId', 'userName', 'content', 'score',
              'thumbsUpCount', 'reviewCreatedVersion', 'at']

# Создайте файл CSV и запишите данные
with open('UK_rew.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Запишите заголовки
    writer.writeheader()

    # Запишите данные из каждого словаря, пропуская дополнительные поля
    for review in result:
        filtered_review = {key: review[key]
                           for key in fieldnames if key in review}
        writer.writerow(filtered_review)
