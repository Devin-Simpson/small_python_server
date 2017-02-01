These are the install instructions for everything I use:

python 2.7:

MySQL:
brew install mysql

MySQL for python:
pip install MySQL-python (this requires a version of pip installed for Python)



To set up the server:

you will need to create your own database in your local MySQL to store the data, you can name it
whatever you want but keep a note of it

you will need to update the information in `login.txt` particularly the username, password, and
database that your MySQL server is using to serve the graph data, my information is in that file
now as a reference for you to fill in, you can also update the host or portnumber if you wish to
do so


setup the database by running `python setup_database.py` before starting the server

start the server by running `python server.py`

access the web application by going to your browser and typing localhost:(your port number)
(ex: localhost:8000)


the graph is build with dygraphs `http://dygraphs.com/` and has some basic interactive features
including mouseover highlighting, zooming both vertically and horizontally by clicking and dragging
the moust, and reseting the view by double clicking the mouse


NOTE: I did not write any of the code for the files in the "Vendor" directory