import sys, getopt
from alchemynewsparser import *

def main(argv):
	fromDate = 1478304000
	toDate = 1478991600
	query = "shooting"
	output = 'news.dat'
	api_key = "YOUR_API_KEY"
	try:
		opts, args = getopt.getopt(argv,"hf:t:q:a:o:",["fromdate=","todate=", "querytext=", "apikey=", "output="])
	except getopt.GetoptError:
		print 'get_news.py -f <fromdate> -t <todate> -q <querytext> -a <apikey> -o <output>'

	for opt, arg in opts:
		if opt == '-h':
			print 'get_news.py -f <fromdate> -t <todate> -q <querytext> -a <apikey> -o <output>'
			sys.exit()
		elif opt in ("-f", "--fromdate"):
			fromDate = arg
		elif opt in ("-t", "--todate"):
			fromDate = arg
		elif opt in ("-q", "--querytext"):
			query = arg
		elif opt in ("-a", "--apikey"):
			api_key = arg
		elif opt in ("-o", "--output"):
			output = arg

	if api_key == "YOUR_API_KEY":
		print "Either enter you Watson News API Key as arguemnt with -a or edit in the main.py. Run main.py -h to see available options."
		sys.exit()
	parser = AlchemyNewsParser({'key':api_key})
	parser.fromDateOf(fromDate)
	parser.toDateOf(toDate)
	parser.queryFor(query)

### the convertor is literally using the same class.... just running the conversion part
## you can change the name of files you want to convert etc. here
	parser.convertToJson("news.dat","export.json")
if __name__ == '__main__':
	main(sys.argv[1:])
