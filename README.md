# bikemap
Dublin Bike Mapping of Bike Occupancy

#Developer Instructions



#User Instructions
When the user accesses the homepage, a map is presented to them with markers placed on all the Dublin bike stations across Dublin city. The icons are color coded in order to allow the user to quickly identify the occupancy of an individual station just by looking at it.

Clicking a marker, launches an info window containing up to date station occupancy information. The user will also be presented with an option to display more information.

Clicking more info option, sends a query to the database to retrieve historical information from the database and display it at the bottom of the page using a Google graph. There are three graphs that used to display information for:
  *The average amount of available bikes on an hourly basis for the chosen day
  *The average wait time for an available bike at that station on the chosen day. This is displayed on a 3 hour basis rather than an hourly basis.
  *The average available bikes for each day of the week for the particular station.

Options are displayed above the graphs that allow the user to query information for each day of the week.
