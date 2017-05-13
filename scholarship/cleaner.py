import HTMLParser,re


def clean(text):
	#1: Escaping HTML characters
	html_parser=HTMLParser.HTMLParser()
	text=html_parser.unescape(text)
	#2: Decoding Data
	text=text.encode('utf-8',errors='ignore')
	#removing urls
	text= re.sub(r"http\S+", "", text)
	#removing user mentions
	text=' '.join(re.sub("(@[A-Za-z0-9_]+)|([^0-9A-Za-z_ \t])|(\w+:\/\/\S+)"," ",text).split())
	return text






'''
#3Apostrophe lookup
APPOSTROPHES={"'s":"is" , "'re":"are"}
words=text.split()
reformed=[APPOSTROPHES[word] if word in APPOSTROPHES else word for word in words]
text=" ".join(reformed)
#7: Spilt attached words
text=" ".join(re.findall('[A-Z][^A-Z]*',text))
#9 Standardiding words
text=".join(".join(s)[:2] for _,s in itertools.groupby(text)
'''