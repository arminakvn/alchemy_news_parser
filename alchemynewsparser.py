import json
from watson_developer_cloud import AlchemyDataNewsV1, watson_developer_cloud_service
import time
import datetime


class AlchemyNewsParser(object):
	"""docstring for AlchemyNewsParser"""
	def __init__(self, arg):
		self.application_state = dict()
		self.application_state.update({"call_count": 0})
		self.application_state.update({"task_log": "parser init"})
		self.arg = arg
		self.alchemy_data_news = AlchemyDataNewsV1(api_key=self.arg["key"])
		self.news_doc_responds = list()
		self.next = 'None'
		self.url_base_url = "https://access.alchemyapi.com/calls/data/GetNews?"
		self.url_key = "apikey="
		self.url_returns = "&return="
		self.retrun_fields_default = "enriched.url.title,enriched.url.url,enriched.url.enrichedTitle.entities,enriched.url.enrichedTitle.docSentiment,enriched.url.enrichedTitle.concepts"
		self.url_start_date = "&start="
		self.url_end_date = "&end="
		self.url_q_field = "&q."
		self.q_field_default = "enriched.url.cleanedTitle="
		self.url_count = "&count="
		self.url_outputMode = "&outputMode=json"

	def urlMaker(self):
		"""alternatively, use requests library to call the api directly and 
		without using the watson cloud developers library"""
		self.made_url = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}".format(self.url_base_url, self.url_key,self.arg["key"],self.url_returns,self.retrun_fields_default,self.url_start_date,self.start,self.url_end_date,self.end,self.url_q_field,self.q_field_default,self.text_for_query,self.url_outputMode)
		# print self.made_url
	def fromDateOf(self, start_date):
		self.start="%s" % (start_date)

	def toDateOf(self, end_date):
		self.end="%s" % (end_date)
	
	def queryFor(self, text_for_query):
		self.text_for_query = text_for_query
	
		
	def checkStatusAndSave(self, results, fw):
		doc_resp = dict()
		print "checking status"
		if results["status"] == "OK":
			self.application_state.update({"task_log": "results status ok, saving ..."})
			print self.application_state
			doc_resp.update({'page_number': self.application_state["call_count"], 'result': results["result"]})
			json.dump(doc_resp,fw)
			fw.write("\n")
			fw.flush()

	def checkNext(self,results):
		self.application_state.update({"task_log": "checking results.next to see if empty"})
		try:

			if results["result"]["next"] != '':
				self.application_state.update({"task_log": "results.next is not empty"})
				print self.application_state
				self.next = results["result"]["next"]
			else:
				self.application_state.update({"task_log": "setting self.next to None before break"})
				print self.application_state
				self.next = 'None'
				self.still_more = False
				return "break"
		except:
			self.next = 'Done'
			self.application_state.update({"task_log": "Checking next failed -- setting to Done"})
			print self.application_state
			return "break"
	
	def getNews(self, fw):
		page_number = 0
		self.still_more = True
		self.application_state.update({"task_log": "getNews method started"})

		print self.application_state

		
		while self.still_more:
			time.sleep(9)
			print "self.next", self.next
			if (self.next == 'None') and (self.next != "Done"):
				try:
					self.application_state.update({"task_log": "next is none, trying the first call"})
					print self.application_state
					results = self.alchemy_data_news.get_news_documents(
						start=self.start,
						end=self.end,
						return_fields=['enriched.url.title',
										'enriched.url.url',
										'enriched.url.author',
										'enriched.url.publicationDate'],
						query_fields={"enriched.url.title={0}".format(self.text_for_query)})
					self.application_state["call_count"] += 1
					self.checkStatusAndSave(results, fw)
					checkBreak = self.checkNext(results)
					if checkBreak == "break":
						break
				except watson_developer_cloud_service.WatsonException:
					self.application_state.update({"task_log": "First call try failed"})
					print self.application_state
					print watson_developer_cloud_service.WatsonException
			elif self.next != "Done":
				print "else of the check for next"
				try:
					self.application_state.update({"task_log": "try with a next-- before call"})
					print self.application_state
					results = self.alchemy_data_news.get_news_documents(
						start=self.start,
						end=self.end,
						return_fields=['enriched.url.title',
										'enriched.url.url',
										'enriched.url.author',
										'enriched.url.publicationDate'],
						query_fields={"enriched.url.title={0}".format(self.text_for_query)},
						next_page=self.next)
					self.application_state["call_count"] += 1
					self.checkStatusAndSave(results, fw)
					self.checkNext(results)

				except watson_developer_cloud_service.WatsonException:
					self.application_state.update({"task_log": "try with a next-- call failed"})
					print self.application_state
					print watson_developer_cloud_service.WatsonException
			else:
				self.still_more = False
				break

	def printResults(self):
		print(self.news_doc_responds)




