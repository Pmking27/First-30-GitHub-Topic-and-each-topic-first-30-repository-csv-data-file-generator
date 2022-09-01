from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def parse_star_count(star_tag):
    star_tag = star_tag.text
    if star_tag[-1] == "k":
        return int(float(star_tag[:-1])*1000)
    return int(star_tag)


url = "https://github.com/topics"

reps = requests.get(url, "htmp.parser")

soup = BeautifulSoup(reps.text, "html.parser")

selection_class = "f3 lh-condensed mb-0 mt-1 Link--primary"

all_topic_tag = soup.find_all('p', {"class": selection_class})

selection_class = "f5 color-fg-muted mb-0 mt-1"

all_topic_desp_tag = soup.find_all('p', {"class": selection_class})

selection_class = "no-underline flex-1 d-flex flex-column"


all_topic_link_tag = soup.find_all('a', {"class": selection_class})

topic_list = []
for topic in all_topic_tag:
    topic_list.append(topic.text)

topic_desp_list = []
for desp in all_topic_desp_tag:
    topic_desp_list.append(desp.text.strip())

topic_link_list = []
for link in all_topic_link_tag:
    topic_link_list.append(f"https://github.com{link['href']}")

topic_dist = {
    'topic': topic_list,
    'description': topic_desp_list,
    'link': topic_link_list
}

data = pd.DataFrame(topic_dist)
data.to_csv('github topic.csv')

for i in range(len(topic_link_list)):
    title = topic_list[i]

    topic_page_url = topic_link_list[i]

    resp = requests.get(topic_page_url)

    topic_doc = BeautifulSoup(resp.text, "html.parser")

    selection_class = "f3 color-fg-muted text-normal lh-condensed"
    repo_tag = topic_doc.find_all('h3', {"class": selection_class})

    username_list = []
    repo_name_list = []
    repo_url_list = []
    star_count_list = []

    for j in range(len(repo_tag)):
        a_tag = repo_tag[j].find_all('a')

        username = a_tag[0].text.strip()
        username_list.append(username)

        repo_name = a_tag[1].text.strip()
        repo_name_list.append(repo_name)

        repo_url = f"https://github.com{a_tag[1]['href']}"
        repo_url_list.append(repo_url)

        star_tag = topic_doc.find_all(
            'span', {"id": "repo-stars-counter-star"})

        star_count = parse_star_count(star_tag=star_tag[j])
        star_count_list.append(star_count)

    repo_dist = {
        'username': username_list,
        'repository name': repo_name_list,
        'repository url': repo_url_list,
        'repository star': star_count_list}

    data = pd.DataFrame(repo_dist)
    data.to_csv(f"{title}.csv")
    time.sleep(1)
