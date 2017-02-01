#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import sys
import json
import datetime
from time import mktime
import MySQLdb


def setupServer():

	PORT_NUMBER = None
	DB_HOST = ""
	DB_USER = ""
	DB_PASSWORD = ""
	DB_NAME = ""

	# read login.txt
	with open("login.txt") as loginFile:
		for line in loginFile:
			line = line.split("=")

			if(line[0] == "portnumber"):
				PORT_NUMBER = int(line[1])
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
	return PORT_NUMBER, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
	

# set up datetime format
date_time_format = "%Y/%m/%d %H:%M:%S"

class requestHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):

		# serve home page
		if self.path == "/":
			self.path = "Static_Files/index.html"
			
		# the service that the AJAX call will hit in order to get the data fror the graph
		if self.path == "/graphdata":
			self.sendJSONResponse()

		mimetype = None
		
		# serve static files
		if self.path.endswith(".html"):
			mimetype="text/html"
		if self.path.endswith(".js"):
			mimetype="application/javascript"
		if self.path.endswith(".css"):
			mimetype="text/css"

		# if a valid static file is requested, serve the file
		if mimetype is not None:
			self.sendPage(mimetype)
			

	def sendPage(self, mimetype):
		reponseFile = open(curdir + sep + self.path) 

		self.send_response(200)
		self.send_header("Content-type", mimetype)
		self.end_headers()	
		self.wfile.write(reponseFile.read())
		reponseFile.close()

	def sendJSONResponse(self):
		graph_data = self.generateJSONGraphData()
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()

		self.wfile.write(json.dumps(graph_data))

	def generateJSONGraphData(self):

		# cursor to database
		cur = db.cursor()

		# set up the JSON data object that will be returned
		JSONdata = {}

		# retrive the data for each topic, insert the indivdual topic data into the graph data JSON object
		graph_data = []
		labels = ["Date"]
		buttons = []
		visibility = []

		topic_names = "" 

		for i in range(0, 50):

			topic_names += "t"+str(i)+", "

			topic_words = ""
			cur.execute("select word from topics_table where topic_id = "+str(i))
			for row in cur.fetchall():
				topic_words += str(row[0]) + ","

			topic_words = str(i) + ": " + topic_words[:-1]
			labels.append("t"+str(i)+":")
			buttons.append(topic_words)
			visibility.append(True)


		topic_names = topic_names[:-2]
		cur.execute("select article_date, "+ topic_names +" from document_topic_distributions_table ORDER BY article_date;")
		for row in cur.fetchall():
			current_row = list(row)
			current_date = row[0].strftime(date_time_format)
			current_row[0] = current_date

			graph_data.append(current_row)
			

		JSONdata["graphdata"] = graph_data
		JSONdata["labels"] = labels
		JSONdata["buttons"] = buttons
		JSONdata["visibility"] = visibility

		return JSONdata
	
try:

	PORT_NUMBER, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME = setupServer()

	# first establish database connection	
	print "connecting to MySQL..."
	db = MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWORD,db=DB_NAME)
	print "connection to MySQL finished, starting server..."

	# establish the server, listening on the specifed port number, with the custom built handler
	server = HTTPServer(("", PORT_NUMBER), requestHandler)
	print "Started httpserver on port " , PORT_NUMBER
	
	# Wait forever for incoming http requests
	server.serve_forever()

# shut down the server with Crtl + C keyboard command
except KeyboardInterrupt:
	print "^C received, shutting down the web server"
	db.close()
	server.socket.close()
