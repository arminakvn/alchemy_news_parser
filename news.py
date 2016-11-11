import json
from watson_developer_cloud import AlchemyDataNewsV1
import time
import datetime



class AlchemyNewsParser(object):
	"""docstring for AlchemyNewsParser"""
	def __init__(self, arg):
		self.arg = arg
		alchemy_data_news = AlchemyDataNewsV1(api_key=self.arg["key"])

	def fromDateOf(self, start_date):
		self.start="%s" % (start_date)

	def toDateOf(self, end_date):
		self.end="%s" % (end_date)
	def queryFor(self, text_for_query):
		self.text_for_query = text_for_query
	def getNewsFor(self, q_field, r_fields):
		results = alchemy_data_news.get_news_documents(
			start=self.start,
			end=self.end,
			return_fields=['enriched.url.title',
							'enriched.url.url',
							'enriched.url.author',
							'enriched.url.publicationDate'],
			query_fields={"enriched.url.title={0}".format(self.text_for_query)})
		self.results = results
				

parser = AlchemyNewsParser({'key':"01c353b6015cd13b7685b7c0c42feea3686df75c"})




filename = datetime.datetime.now().strftime("%Y%m%d-%H")
print(datetime.datetime.now())
alchemy_data_news = AlchemyDataNewsV1(api_key='01c353b6015cd13b7685b7c0c42feea3686df75c')

# results = alchemy_data_news.get_news_documents(start='now-30d', end='now', time_slice='12h')
# print(results,json.dumps(results, indent=2))

results = alchemy_data_news.get_news_documents(
    start='1473441494',
    end='1478711895',
    return_fields=['enriched.url.title',
                   'enriched.url.url',
                   'enriched.url.author',
                   'enriched.url.publicationDate'],
    query_fields={'enriched.url.title=shooting'})
print(json.dumps(results, indent=2))
with open('results/'+ filename +'alchemy.json', 'w') as f:
	json.dump(results, f, indent=2)






