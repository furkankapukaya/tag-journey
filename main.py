# etiket_index/etiket_type
# siyaset, seyahat, yemek, egitim, spor, araba, bilgisayar, hayvan, insan, doga, bilim, uzay, tarih, vergi,
# saglik, renk, muzik, yazilim, iletisim, ulasim, savas, sinema, tiyatro, kitap, cografya, kariyer, moda,

import null as null
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
import time
import helpers as localhelpers

SCROLL_PAUSE_TIME = 4
SITE_LOAD_TIME = 3
driver = webdriver.PhantomJS()
tags = []
# doc_type = 'etiket_type'
# es_index = 'etiket_index'
# done 'siyaset', 'seyahat', 'yemek', 'egitim', 'spor', 'araba', 'bilgisayar', 'hayvan', 'insan', 'doga', 'bilim','tarih', 'saglik', 'muzik', 'yazilim',  'savas', 'sanat', 'cografya', 'moda'
# undone
es = Elasticsearch()
doc_type = 'etiket_type'
doc_id = 1
es_index = 'etiket_index'
# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
# # print(res['created'])
#
# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])
#
# es.indices.refresh(index="test-index")
#
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


for tag in tags:
    driver.get('https://medium.com/search')
    time.sleep(SITE_LOAD_TIME)
    # Siradaki tag icin arama yap
    driver.find_element_by_class_name("js-searchInput").send_keys(tag)
    driver.find_element_by_class_name("js-searchInput").send_keys(Keys.ENTER)
    time.sleep(SITE_LOAD_TIME)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # yeni sayfa uzunlugu
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Search Tag sonrasi gelen sonuclarin linklerini kaydet
    # article_elements = driver.find_elements_by_class_name("postArticle-readMore")
    article_elements = driver.find_elements_by_class_name("postArticle-content")
    print(tag + " :" + str(len(article_elements)))

    links = []
    for article_element in article_elements:
        new_link = article_element.find_element_by_css_selector('a').get_attribute('href')
        links.append(new_link)

    # Yeni linklerdeki icerikleri kaydet
    for link in links:
        driver.get(link)
        time.sleep(SITE_LOAD_TIME)

        # get title
        try:
            tag_element = driver.find_element_by_class_name("graf--title")
            title = tag_element.get_attribute('innerHTML').encode('utf-8')
            title = localhelpers.cleanhtml(title)
        except:
            title = "Unknown Title"
        #print(title)

        # get content
        try:
            tag_element = driver.find_element_by_class_name("postArticle-content")
            p_tags = []
            p_tags = tag_element.find_elements_by_css_selector('p')
            content = ""
            for p_tag in p_tags:
                content += (p_tag.get_attribute('innerHTML')).encode('utf-8')
            content = localhelpers.cleanhtml(content)
            #print content
        except:
            content = "Unknown Content"

        # get tags
        content_tags = []
        try:
            tag_element = driver.find_element_by_class_name("js-postTags")
            tag_hrefs = []
            tag_hrefs = tag_element.find_elements_by_css_selector('a')
            for tag_href in tag_hrefs:
                # print(tag_href.get_attribute('innerHTML'))
                content_tags.append(tag_href.get_attribute('innerHTML').encode('utf-8'))
            # print(content_tags)
        except:
            pass
        doc = {
            'title': title,
            'content': content,
            'tags': content_tags,
            'parentCategory': tag,
        }
        # print(doc)
        res = es.index(index=es_index, doc_type=doc_type, body=doc)
        # doc_id += 1


'''
driver = webdriver.PhantomJS()
very_first_tag = "mutluluk"
old_links = []

tags = []
old_tags = []
tags.append(very_first_tag)
stop_count = 0

while len(tags) > 0 and stop_count < 10:
    tag = tags.pop(0)
    stop_count += 1
    print("Aranan tag : " + tag)
    old_tags.append(tag)
    # Arama sayfasini ac
    driver.get('https://medium.com/turkce/search')
    time.sleep(2)
    # Siradaki tag icin arama yap
    driver.find_element_by_class_name("js-searchInput").send_keys(tag)
    driver.find_element_by_class_name("js-searchInput").send_keys(Keys.ENTER)
    time.sleep(2)

    # Search Tag sonrasi gelen sonuclarin linklerini kaydet
    article_elements = driver.find_elements_by_class_name("postArticle-readMore")
    links = []
    for article_element in article_elements:
        new_link = article_element.find_element_by_css_selector('a').get_attribute('href')
        if new_link not in old_links:
            links.append(new_link)

    # Yeni linklerdeki tagleri kaydet
    for link in links:
        old_links.append(link)
        driver.get(link)
        time.sleep(2)
        tag_element = driver.find_element_by_class_name("js-postTags")
        tag_hrefs = []
        tag_hrefs = tag_element.find_elements_by_css_selector('a')
        for tag_href in tag_hrefs:
            tmp_tag = tag_href.get_attribute('innerHTML')
            if tmp_tag not in tags and tmp_tag not in old_tags:
                tags.append(tmp_tag)
                print(tmp_tag)
'''
