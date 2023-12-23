# django-tutorial
- See the first 1hr of the course on Youtube here: [Python Django Tutorial for Beginners](https://www.youtube.com/watch?v=rHux0gMZ3Eg) 
- Purchase the full course here: [The Ultimate Django Series](https://codewithmosh.com/p/the-ultimate-django-series) 

## Django Commands
```sh
pip install django
django-admin startproject storefront .
python manage.py runserver 9000
python manage.py startapp playground # make a new app

#---------------make migrations
python ./manage.py makemigrations # remember to rerun this if we change any of the db models
# if you rerun after a change this will create a new migration file for you
# if you rename a file after a migration -> you must find all the dependencies and rename them too (unless it's the most recent migration => there will be no dependencies)
# what if changes aren't detected -> make sure the app is in the INSTALLED_APPs
# for custom sql:
python ./manage.py makemigrations store --empty


#--------------running migrations
python ./manage.py migrate
python ./manage.py migrate store 0005 # revert back to prev migration
python ./manage.py sqlmigrate <migration> # show the actual SQL code
```

## Handy VSCode Shortcuts
- F2 -> rename everywhere
- Cmd+T -> search for a symbol (symbol = class / function / variable)
- Cmd+Shift+O -> search for a symbol in a file

## Definitions
- client vs server
  - client -> run on the client's machine
  - server -> runs on our machine (ex: AWS)
- server vs client side page generation
  - best practice today: client will generate the web page (ex: react, angular, vue)
  - server will just focus on data
- http requests: this is how the client communicates with the server
  - via an endpoints on an API (ex: /products, /orders, ...)
- django project = collection of apps
  - each app should be responsible for one thing (cohesion / focus) 
  - you should have no dependencies between apps 
  - a good design is one with minimal coupling and high cohesion (focus)
- slug = part of url that is used by search engines
  - ex: `get-max-and-min-formatted-values-from-queryset` part of a stackoverflow question 
- ORMs = Object Relational Mappers
  - when pulling a row from a relational database we need to map these rows to objects
  - we used to need to do this by hand (directly querying the database)
  - an ORM frees us from writing a lot of repetitive code
  - enabling us to directly code in Python, which will translate into SQL at runtime
  - We still need to write SQL for complex queries, but for the majority of simple cases we can just use ORMs
  - migrations / models are all apart of django ORM
  - ORMs are good because they reduce the amount of code required - building the best optimized solution is not the goal - it's delivering 

## Recommendations
- Only use SQLite for development


## Cool Resources
- Generating Data -> https://mockaroo.com/
