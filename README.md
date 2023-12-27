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

#--------------admin
python manage.py createsuperuser
# reset password
python manage.py changepassword <username>
```

## Handy VSCode Shortcuts
- F2 -> rename everywhere
- Cmd+T -> search for a symbol (symbol = class / function / variable)
- Cmd+Shift+O -> search for a symbol in a file
- Ctrl+'-' -> jump back to where you were in the code
- Cmd+click -> lookup the definition of a function / class (including imported ones)
- Cmd+Shift+O -> see all the symbols in a module

## Definitions

### client vs server
- client -> run on the client's machine
- server -> runs on our machine (ex: AWS)

### server vs client side page generation
- best practice today: client will generate the web page (ex: react, angular, vue)
- server will just focus on data

### http requests: this is how the client communicates with the server
- via an endpoints on an API (ex: /products, /orders, ...)

### django project = collection of apps
- each app should be responsible for one thing (cohesion / focus) 
- you should have no dependencies between apps 
- a good design is one with minimal coupling and high cohesion (focus)

### slug = part of url that is used by search engines
- ex: `get-max-and-min-formatted-values-from-queryset` part of a stackoverflow question 

### ORMs = Object Relational Mappers
- when pulling a row from a relational database we need to map these rows to objects
- we used to need to do this by hand (directly querying the database)
- an ORM frees us from writing a lot of repetitive code
- enabling us to directly code in Python, which will translate into SQL at runtime
- We still need to write SQL for complex queries, but for the majority of simple cases we can just use ORMs
- migrations / models are all apart of django ORM
- ORMs are good because they reduce the amount of code required - building the best optimized solution is not the goal - it's delivering 

### Managers and QuerySets
- `Product.objects.` every model in django has a manager object
- A manager object is an interface to the database (like a remote control with a bunch of buttons to talk to our database)
- `query_set = Product.objects.all() # returns all the objects in the database`
- Query Set = object that encapsulates a query
  - At some point django will evaluate the queryset to create the right query to send to our database
- When does Django evaluate the query set
  - when we iterate over it
  - when we call `list(query_set)` on it
  - access an indvidual element `query_set[3]`
  - slice it -> `query_set[3:5]`
  - they're lazy -> only evaluated when they need to be
- We can also change methods together to build a more complex query
  - `query_set.filter().filter().order_by()`
  - then at some point when we iterate over it or slice it or ... then it will be evaluated

### RESTful APIs
- API = interface that client apps can use to get or save data
  - like a remote control with a bunch of buttons for different functionality
- Each endpoint will have it's own functionality
  - ex: get or save products, orders, shopping carts, ...
- REST = short for Representational State Transfer
  - In practical terms its a set of rules for clients and servers to communicate over the web
  - These rules help us build systems that are:
    -  Fast
    -  Scalable
    -  Reliable
    -  Easy to understand
    -  Easy to change
-  Resources = like an object in our application (product, collection, shopping cart, ...)
   - Available on the web and client applications can access them using a URL, Exs:
   - http://website.com/products
   - http://website.com/products/1
   - http://website.com/products/1/reviews
   - http://website.com/products/1/reviews/1
   - generally best not to nest beyond this
- Resource Representations
  - Exs: HTML, XML, JSON
  - But these aren't the representations on server, we transfer into this so the clients can understand the output
- HTTP Methds
  - When building a RESTful API we expose 1+ endpoints for clients
  - Each endpoint can support multiple operations (ex: read / write / ...)
  - HTTP Methods
    - Get (read)
    - Post (write)
    - Put (update)
    - Patch (updating part of it)
    - Delete (delete)
- Create a Product
  - Send a post request to the `/products` endpoint
  - Specify the product details in the body of the request
    - `{"title": "", "price": 10}`
- Updating a Product
  - Update all properties => `PUT /products/1`
  - Update some properties => `PATCH /products/1`
- Deleting a Product
  - `DELETE /products/1`
- Serializers
  - converts a model instance to a dictionary
  - options for serializing
    - Primary Key
    - String
    - Nested Object
    - Hyperlink

### Advanced API Concepts
- Building an API:
  1. Create a Serializer
  2. Create a View
  3. Register a route


## Recommendations
- Only use SQLite for development


## Cool Resources
- Generating Data -> https://mockaroo.com/
