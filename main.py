from alchemynewsparser import *



if __name__ == '__main__':


	parser = AlchemyNewsParser({'key':"01c353b6015cd13b7685b7c0c42feea3686df75c"})

	# parser.fromDateOf(1473441494)
	parser.fromDateOf(1478711800)
	
	parser.toDateOf(1478711895)
	
	parser.queryFor("shooting")
	
	parser.getNews()
	
	parser.printResults()