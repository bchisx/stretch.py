import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import pandas as pd
import time
from datetime import datetime, timedelta

def make_snapshot(terms):
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    url_one = "https://mastodon.social/api/v1/timelines/public?limit=40"
    url_two = "https://mastodon.cloud/api/v1/timelines/public?limit=40"
    url_three = "https://mstdn.social/api/v1/timelines/public?limit=40"
    url_four = "https://pawoo.net/api/v1/timelines/public?limit=40"
    url_five = "https://mastodon.online/api/v1/timelines/public?limit=40"
    url_six = "https://mastodon.xyz/api/v1/timelines/public?limit=40"
    params = {"limit": 40}

    def fetch_posts(params, url):
        try:
            r = requests.get(url, allow_redirects=False, headers=header, timeout=5, params=params)
            return json.loads(r.text)
        except:
            print("summon fail")
            pass
    # Initial fetch for recursive function
    json_data = fetch_posts(params, url_one)

    def scan(deg, url, json_data=json_data):
        params["max_id"] = str(int(json_data[-1]["id"]) - deg)
        try:
            json_data = fetch_posts(params, url)
        except:
            print("scan fail")
            json_data = json_data
        return json_data

    i = 0
    all_posts = []
    while i <= 50:
        if i < 17:
            deg = 100000000000 * i
        elif i < 35:
            deg = 1000000000000 * i
        else:
            deg = 10000000000000 * i

        all_posts.append(scan(deg, url_one))
        all_posts.append(scan(deg, url_two))
        all_posts.append(scan(deg, url_three))
        all_posts.append(scan(deg, url_four))
        all_posts.append(scan(deg, url_five))
        all_posts.append(scan(deg, url_six))
        i += 1
        time.sleep(10)
    
    formatted_posts = []
    for batch in all_posts:
        try:
            posts=[]
            times=[]
            for profile in batch:
                post=profile["content"]
                this_time=profile["created_at"]
                popularity=profile["favourites_count"]
                virality=profile["reblogs_count"]
                posts.append(post)
                times.append(this_time)
                soup = BeautifulSoup(post, 'html.parser')
                text_content = soup.get_text()
                formatted_posts.append({
                    "content": text_content,
                    "created_at": this_time,
                    "favourites_count": popularity,
                    "reblogs_count": virality
                })
        except: 
            print("format fail")
            continue
    
    print("whew, made it. posts have been fetched and formatted. now for the dupes.") 

    seen_content = set()
    results = []
    for item in formatted_posts:
        try:
            if item["content"] not in seen_content:
                results.append(item)
                seen_content.add(item["content"])
        except:
            continue

    #unique_posts = []
    #for item in results:
    #    if item not in unique_posts:
    #        unique_posts.append(item)
    
    return results

import spacy
from collections import Counter, defaultdict

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def find_top_words(snapshot_data, top_n=100):
    action_words = []
    topics = []
    famous_things = []

    # Process each post's content
    for item in snapshot_data:
        doc = nlp(item["content"])
        for token in doc:
            if token.is_alpha and not token.is_stop:
                if token.pos_ == "VERB":
                    action_words.append(token.lemma_.lower())
                elif token.pos_ == "NOUN":
                    topics.append(token.lemma_.lower())
                elif token.pos_ == "PROPN":
                    famous_things.append(token.lemma_)

    # Count the frequency of each word
    action_word_freq = Counter(action_words)
    topic_freq = Counter(topics)
    famous_things_freq = Counter(famous_things)

    # Get the top N most common words
    top_action_words = action_word_freq.most_common(top_n)
    top_topics = topic_freq.most_common(top_n)
    top_famous_things = famous_things_freq.most_common(top_n)

    # Print the top words
    print("Top Action Words:")
    for word, freq in top_action_words:
        print(f"{word}: {freq}")

    print("\nTop Topics:")
    for word, freq in top_topics:
        print(f"{word}: {freq}")

    print("\nTop Famous Things:")
    for word, freq in top_famous_things:
        print(f"{word}: {freq}")

def find_pop_words(snapshot_data, top_n=100):
    action_words = defaultdict(int)
    topics = defaultdict(int)
    famous_things = defaultdict(int)

    # Process each post's content
    for item in snapshot_data:
        doc = nlp(item["content"])
        popularity = item.get("favourites_count", 0)
        virality = item.get("reblogs_count", 0)
        weight = popularity + virality

        for token in doc:
            if token.is_alpha and not token.is_stop:
                if token.pos_ == "VERB":
                    action_words[token.lemma_.lower()] += weight
                elif token.pos_ == "NOUN":
                    topics[token.lemma_.lower()] += weight
                elif token.pos_ == "PROPN":
                    famous_things[token.lemma_] += weight

    # Get the top N words by weighted score
    top_action_words = sorted(action_words.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_famous_things = sorted(famous_things.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Print the top words
    print("Top Action Words by Popularity and Virality:")
    for word, score in top_action_words:
        print(f"{word}: {score}")

    print("\nTop Topics by Popularity and Virality:")
    for word, score in top_topics:
        print(f"{word}: {score}")

    print("\nTop Famous Things by Popularity and Virality:")
    for word, score in top_famous_things:
        print(f"{word}: {score}")



