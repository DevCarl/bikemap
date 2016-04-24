# bikemap
[Dublin Bike Mapping of Bike Occupancy](http://ec2-52-34-120-212.us-west-2.compute.amazonaws.com/)

#Developer Instructions
The bikemap application backend is written in [Python 3.4](https://docs.python.org/3.4/). [SQLite3](https://www.sqlite.org/) is used to provide basic database functionality. The [Flask](http://flask.pocoo.org/) framework for web application development. [WSGI](https://wsgi.readthedocs.org/en/latest/) for providing the communications interface between the web app and Python backend. [Apache2](https://httpd.apache.org/) to host the webpages and web app.
The bikemap application frontend is written in [HTML5](https://www.w3.org/TR/html5/) and [Javascript](http://www.ecma-international.org/publications/standards/Ecma-262.htm). [Google Maps](https://developers.google.com/maps/documentation/javascript/) and [Google Charts](https://developers.google.com/chart/) APIs are used to provide visualisations of bikerack locations, availability, etc.
Both the frontend and the backend use the [JCDecaux Dublin Bikes API](https://developer.jcdecaux.com/#/opendata/vls?page=getstarted) to gather bike information. The frontend displays live data requests from the API. The backend requests data every 5mins and saves to a database for processing.

##Install 

###Local Install

To run a local instance of the application, simply download the applicaton files from the github directory: https://github.com/harneyp2/bikemap

After downloading the file, run the application from the command line using `python application.py`. Note that you will need Flask installed in order to run the application. Once the application has begun to run the interface can be accessed through the broswer from your localhost at: http://127.0.0.1:5000

###Server Install

The following steps describe the process to run the application in a *Ubuntu Linux* environment. The locations and steps may differ in other environments.
Install *python3*, *python3-pip*, *apache2* and *libapache2-mod-wsgi-py3* using `apt-get install`.
Install *flask* and *sqlite3* using `pip3 install`

The entire package should be placed inside the */var/www/html/* where it can be hosted by the *Apache* server. The file _ec2*******.com.conf_ contains the configuration for the Apache Virtual Host and must be copied to */etc/apache2/sites-available/*. The file is configured for a specific domain name. The *filename* and *ServerName* within the script must be changed to reflect the domain name of the target server. Restart apache `service apache2 restart`

If you wish to gather new data `python3 /bikemap/bike_scraper/__init__.py &`, the application will connect to the *JCDecaux API* every 5mins and leave the shell accessible.

#Testing 

In order to run our tests, you can navigate to the tests folder using the command line. From there, you can enter in nosetests and it will do the work for you. Nosetests is required to implement the tests part of this.

The tests created for our Bike Scraper project test for the base cases of our database functionality. In order, it will test if a database has been created, if it is created empty and will test that we can fetch information from the Bike_Scraper API.

Finally, we complete a set up to build a database off of a test database to test if we can actually insert data into our database. During teardown, we remove the new database that has been created for these tests and rename the completed.txt into Data.txt so our tests are completely re-usable.

We decided that the basic functionality of the database is the most important part of our project to test as it is the centre of where we place and retrieve data from. For all other aspects, such as the Javascript and Python, we implemented a validation stage and passed our code over to another member of the team to test, once it had passed inspection from the impartial member of the team, it could be moved into our completed stage.

#User Instructions
When the user accesses the homepage, a map is presented to them with markers placed on all the Dublin bike stations across Dublin city. The icons are color coded in order to allow the user to quickly identify the occupancy of an individual station just by looking at it.

Clicking a marker, launches an info window containing up to date station occupancy information. The user will also be presented with an option to display more information.

Clicking more info option, sends a query to the database to retrieve historical information from the database and display it at the bottom of the page using a Google graph. There are three graphs that used to display information for:
  * The average amount of available bikes on an hourly basis for the chosen day
  * The average wait time for an available bike at that station on the chosen day. This is displayed on a 3 hour basis rather than an hourly basis.
  * The average available bikes for each day of the week for the particular station.

Options are displayed above the graphs that allow the user to query information for each day of the week.
