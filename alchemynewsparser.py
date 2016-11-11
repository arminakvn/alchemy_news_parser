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

	def fromDateOf(self, start_date):
		self.start="%s" % (start_date)

	def toDateOf(self, end_date):
		self.end="%s" % (end_date)
	
	def queryFor(self, text_for_query):
		self.text_for_query = text_for_query
	
		
	def checkStatusAndSave(self, results):
		doc_resp = dict()
		print "checking status"
		if results["status"] == "OK":
			self.application_state.update({"task_log": "results status ok, saving ..."})
			print self.application_state
			doc_resp.update({'page_number': self.application_state["call_count"], 'result': results["result"]})
			self.news_doc_responds.append(doc_resp)

	def checkNext(self,results):
		self.application_state.update({"task_log": "checking results.next to see if empty"})
		try:

			if results["result"]["next"] != '' and results["result"]["next"] != self.next:
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
			self.next = 'None'
			return "break"
	
	def getNews(self):
		page_number = 0
		self.still_more = True
		self.application_state.update({"task_log": "getNews method started"})

		print self.application_state

		
		while self.still_more:
			time.sleep(9)
			# page_number += 1
			# try:
			print "self.next", self.next
			if self.next == 'None':
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
						query_fields={"enriched.url.title={0}".format(self.text_for_query)},
						next_page=self.next)
					self.application_state["call_count"] += 1
					self.checkStatusAndSave(results)
					checkBreak = self.checkNext(results)
					if checkBreak == "break":
						break
					# return results




				except watson_developer_cloud_service.WatsonException:
					self.application_state.update({"task_log": "First call try failed"})
					print self.application_state
					print watson_developer_cloud_service.WatsonException
			else:
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
						query_fields={"enriched.url.title={0}".format(self.text_for_query)})
					self.application_state["call_count"] += 1
					# return results
					self.checkStatusAndSave(results)
					self.checkNext(results)

				except watson_developer_cloud_service.WatsonException:
					self.application_state.update({"task_log": "try with a next-- call failed"})
					print self.application_state
					print watson_developer_cloud_service.WatsonException
					# self.still_more = False
					# break
					# self.results = results
			
			# except:
			# 	pass
	def printResults(self):
		print(self.news_doc_responds)




