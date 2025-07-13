import json
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get("https://steamdb.info/tags/")

time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

tags_dict = {}

for div in soup.select("div.label"):
	a_tag = div.find("a", href=True)
	if a_tag:
		match = re.search(r"/tag/(\d+)/", a_tag["href"])
		if match:
			tag_id = match.group(1)
			emoji_span = a_tag.find("span", attrs={"aria-hidden": "true"})
			if emoji_span:
				emoji_span.extract()
			tag_name = a_tag.get_text(strip=True)
			tags_dict[tag_id] = tag_name

driver.quit()

tags_dict = dict(sorted(tags_dict.items(), key=lambda x: int(x[0])))

with open("steamdb_tags.json", "w", encoding="utf-8") as f:
	json.dump(tags_dict, f, ensure_ascii=False, indent=2)