from bs4 import BeautifulSoup
import lxml
import requests
import json

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                  "Safari/537.36 "
}

fest_link_urls = []

for i in range(0, 144, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May "
    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data["html"]

    # with open(f"data/index_{i}.html", "w") as f:
    #     f.write(html_response)

    with open(f"data/index_{i}.html") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    links = soup.find_all("a", class_="card-img-link")
    for link in links:
        fest_url = "https://www.skiddle.com/" + link.get("href")
        fest_link_urls.append(fest_url)

fest_dict = {}
count = 0

for url in fest_link_urls:
    req = requests.get(url, headers=headers)
    print(f"{count} count")
    try:
        print(url)
        soup = BeautifulSoup(req.text, "lxml")
        fest_info_block = soup.find("div", class_="top-info-cont")
        fest_name = fest_info_block.find("h1").text.strip()
        fest_date = fest_info_block.find("h3").text.strip()
        fest_location = "https://www.skiddle.com/" + fest_info_block.find("a", class_="tc-white").get("href")

        data = {
            "fest_name": fest_name,
            "fest_date": fest_date,
            "fest_location": fest_location
        }

        fest_dict = data

        with open(f"data/festivals.json", "a") as f:
            json.dump(data, f, indent=4)

        count += 1
    except Exception as ex:
        print(ex)