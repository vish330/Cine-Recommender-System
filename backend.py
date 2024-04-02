import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import math

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

def calc_score(title_no):
    url = "https://www.imdb.com/title/{}/reviews/_ajax?ref_=undefined&paginationKey={}"
    key = ""
    data = {"movie": [], "review": [], "rscore": [], "sscore": [], "result": []}
    while True:
        response = requests.get(url.format(title_no, key))
        soup = BeautifulSoup(response.content, "html.parser")
        pagination_key = soup.find("div", class_="load-more-data")
        if not pagination_key:
            break
        key = pagination_key["data-key"]
        for title, review, rating in zip(
            soup.find_all(class_="title"),
            soup.find_all(class_="text show-more__control"),
            soup.find_all(class_="rating-other-user-rating")
        ):
            review_text = review.get_text()
            sscore = sid.polarity_scores(review_text)['compound'] 
            cscore = (sscore + 1) * 5  
            result = cscore +  float(rating.get_text(strip=True).split('/')[0]) 
            data["movie"].append(title.get_text(strip=True))
            data["review"].append(review_text)
            data["sscore"].append(sscore)
            data["rscore"].append(rating.get_text(strip=True).split('/')[0])
            data["result"].append(result)
        break
    df = pd.DataFrame(data)
    df.to_csv("movies.csv", index=False)
    #print(df)
    df.fillna(0, inplace=True)
    if df.empty:
        return 0
    return math.ceil(df['result'].mean())

def extractmovies(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    df = {"id": [], "title": [], "score": [], "movie_url": []}
    c = 0
    main_div = soup.find('div', class_="ipc-page-grid__item ipc-page-grid__item--span-2")
    if main_div:
        ul = main_div.find("ul")
        if ul:
            for movie in ul.find_all("li"):
                link = movie.find('a', class_="ipc-title-link-wrapper")
                if link:
                    movie_url = "https://www.imdb.com" + link.get('href')
                    movie_response = requests.get(movie_url, headers=headers)
                    movie_soup = BeautifulSoup(movie_response.content, 'html.parser')
                    review_section = movie_soup.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers sc-274f2729-0 gyrnjw baseAlt")
                    if review_section:
                        review_link = review_section.find_all("li")[1].find('a')
                        if review_link:
                            review_url = "https://www.imdb.com" + review_link['href']
                            url_parts = review_url.split('/')
                            title_number = url_parts[4]
                            score = calc_score(title_number)
                            movie_name = movie_soup.find('span', class_="hero__primary-text").get_text()
                            df['score'].append(score)
                            df['id'].append(title_number)
                            df['title'].append(movie_name)
                          

                            df['movie_url'].append(movie_url)
                            c += 1
                if c == 3:
                    break
  
    num_movies = len(df['id'])
    
    
    if num_movies == 0:
        return pd.DataFrame()  
    elif num_movies == 1:
        return pd.DataFrame([df])  
    elif num_movies == 2:
        return pd.DataFrame(df)  
    else:
        
        df = pd.DataFrame(df).sort_values(by='score', ascending=False).head(3)
        return df


def update_dashboard():
    print("Updating dashboard...")
    extractmovies("https://www.imdb.com/search/title/?title_type=feature&genres=animation")


schedule.every().monday.at("00:00").do(update_dashboard)