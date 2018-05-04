from elasticsearch import Elasticsearch

es = Elasticsearch()

page = es.search(index='etiket_index', doc_type='etiket_type')
print(page)