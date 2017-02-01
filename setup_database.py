import MySQLdb


DB_HOST = ""
DB_USER = ""
DB_PASSWORD = ""
DB_NAME = ""

# read login.txt
with open("login.txt") as loginFile:
	for line in loginFile:
		line = line.split("=")

		if(line[0] == "portnumber"):
			continue

		if(line[0] == "host"):
			DB_HOST = line[1].strip()
			continue

		if(line[0] == "user"):
			DB_USER = line[1].strip()
			continue

		if(line[0] == "password"):
			DB_PASSWORD = line[1].strip()
			continue

		if(line[0] == "database"):
			DB_NAME = line[1].strip()
			continue

db = MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWORD,db=DB_NAME)

# setting up all the topics as columns for the distorbution table, 
# using variables so I dont have to write them all out
topicColumns = ""
topicColumnInput = ""
for i in range (0, 50):
	current_index = str(i)
	topicColumns += ", t" + current_index + " FLOAT NOT NULL"
	topicColumnInput += "t" + current_index + ", "

# get rid of the last comma
topicColumnInput = topicColumnInput[:-2]

with db:
	cursor = db.cursor()

	cursor.execute("DROP TABLE IF EXISTS topics_table")
	cursor.execute("CREATE TABLE topics_table (topic_id INT NOT NULL, word VARCHAR(40) NOT NULL,\
	 frequency INT NOT NULL, PRIMARY KEY(topic_id, word));")

	cursor.execute("DROP TABLE IF EXISTS document_topic_distributions_table")
 	cursor.execute("CREATE TABLE document_topic_distributions_table (article_id INT NOT NULL PRIMARY KEY,\
 	 title VARCHAR(500) NOT NULL,article_date DATETIME NOT NULL" + topicColumns + ");")

	skipLine = True

	with open("./topics/topics.txt") as topicsFile:
		for line in topicsFile:

			# skip first line of file 
			if skipLine:

				skipLine = False
				continue

			topic = line.split("	")
			currentTopicID = topic[0]

			# strip off the double quotes surrounding all the words and the last |
			topicWordsAndFrequency = topic[1][1:-4].split("|")
			for currentWordAndFrequency in topicWordsAndFrequency:

				currentLine = currentWordAndFrequency.split(",")
				currentWord = currentLine[0]
				currentFrequency = currentLine[1]

				cursor.execute("INSERT INTO topics_table (topic_id, word, frequency) VALUES(" \
					+ currentTopicID + ", '" + currentWord + "', " + currentFrequency + ");")
				

	skipLine = True

	with open("./topics/document_topic_distributions.txt") as distributionsFile:
		for line in distributionsFile:

			# skip first line of file 
			if skipLine:

				skipLine = False
				continue

			article = line.split("	")
			current_article_id = article[0]
			
			current_title = article[1]
			# escape all quotes 
			current_title = current_title.replace("'", "\\'")
			current_title = current_title.replace('"', '\\"')

			current_article_date = article[2]

			# change format to fit date time
			modified_time_date = current_article_date.split(" ")
			modified_date = modified_time_date[0].split("/")
			current_date = modified_date[2] + "-" + modified_date[0] + "-" + modified_date[1]
			current_time = modified_time_date[1] + ":00"

			current_date_time = current_date + " " + current_time

			# get the probabilities for all topics for the current article
			current_topic_frequency = ""
			for i in range (3, len(article)):
				current_topic_frequency += article[i] + ", "

			# remove the last comma
			current_topic_frequency = current_topic_frequency[:-2]

			cursor.execute("INSERT INTO document_topic_distributions_table (article_id, title, article_date, " \
				+ topicColumnInput + ") VALUES(" + current_article_id +", '" + current_title + "', '" \
				+ current_date_time + "', " + current_topic_frequency +");")

db.close()

print "Completed database setup"