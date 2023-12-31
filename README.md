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

### Authentication
- Middleware = a function that takes a request and passes this to the next middleware or returns a response
  - if it returns a response the next middleware function will not be called 
  - when we recieve a request at some point that will passed to a view at this point it will run through all the middleware functions
  - ex: authentication middleware
  - a request object at runtime will have an attributt called user (either an instance of the anonymous user class or a user object)
- Customizing the user model
  - Extend the user -> using inheritance we can create another model called AppUser that inherits from the user model
    - -> we extend the user table -> any fields on here will be added to the user table
    - Only use this for storing authentication related fields
  - Create a profile -> create a 1:1 link with the user model using composition (profile model is composed of the user model) not inheritance
    - Use this for storing any other fields that aren't related to authentication
    - Ex: sales app can have a Customer profile, an HR app can have an Employee profile, ...
- Always create a custom user module in the beginning of your project -> otherwise you'll have to nuke the db and rebuild it
- Steps to extend the user model:
  - Create a new model that extends AbstractUser
  - In the setting model we set `AUTH_USER_MODEL`` to our new model (`core.User`)
  - Then we stop referencing the user model directly but instead use `settings.AUTH_USER_MODEL`
- Steps to create a user profile
  - create a profile model (ex: Customer)
  - in the profile model make a 1:1 field with the `settings.AUTH_USER_MODEL`
- Groups -> can contain multiple permissions which we can assign users into
  - ex: admin group, customer group, ...
  - we can assign permissions to groups
  - we can assign users to groups

### Securing API Endpoints
- We can secure our API endpoints by adding permissions to our views
- Permissions are rules that determine whether a user can access a resource or not
- This section:
  - Token based authentication -> defacto standard for securing APIs
  - Adding authentication endpoints to our APIs
  - Allow users to register / login / logout
  - Apply permissions to some of our endpoints so they're not accessible to anyone
- Token based authentication
  1. New user registers so on their machine this will send a request to the user endpoint (`/users`)
  2. On our server we will create a account for them user with their username, password, email, ... (`{user}`)
  3. The user needs to login -> the client app needs to send a request to the authentication endpoint (`/auth`) and it will send the username and password (`{un, pw}`) to the server and on the server we'll validate the user credentials -> if not valid we'll return an error but if valid -> we'll return a token (`{token}`) -> this token will be stored on the client machine to access protected resources and everytime they want to access a protected resource they will pass this token with the request to the server
- djoser - useful package for user authentication: https://djoser.readthedocs.io/en/latest/ - but this is just an API layer a bunch of views, serializers and routes so we need an auth engine to do the actual work
- auth engines: https://djoser.readthedocs.io/en/latest/authentication_backends.html
  - token based authentication -> built in django rest framework -> uses a database table to store tokens, so everytime we receive a request on the server we need to query the database to check if the token is valid
  - JSON web token authentication -> doesn't need a database -> because every token has a digital signature and on the server we can verify the signature without needing to query the database
- Registering Users -> client app needs to send a post request to the `/users` endpoint with the user details in the body of the request
- Creating User Profiles -> djoser can't handle this for us, we need to build it ourselves
  - We can add this into the store app bc this is where we defined our customers
- Logging in -> client app needs to send a post request to the `/auth/jwt/create` endpoint with the username and password in the body of the request
  - then this will return 2 tokens: access token and refresh token
    - access token -> used to access protected resources (valid for 5 mins by default)
    - refresh token -> used to get a new access token when the access token expires (valid for 1 day by default)
  - then these will need to be stored in the client - handled by the front end
    - web apps -> stored in browsers local storage
    - mobile apps -> stored in some other kind of local storage
- logging out -> just need to remove the tokens from the client (because we're using jwt)
- jwt (json web tokens) -> (see more here: https://jwt.io/)
  - if tokens are valid -> return the user_id
  - can a hacker regenerate this signature -> yes, but only if they get access to the secret key (which is stored on the server)
- refreshing tokens
  - if the clients needs to access a protected api endpoint it needs to send the access token in the header of the request
  - but if the token is expired -> it will respond with a 401 error (unauthorized)
  - then the client needs to send a post request to the `/auth/jwt/refresh` endpoint with the refresh token in the body of the request to get a new access token
- Getting a user -> client app needs to send a get request to the `/auth/users/me` endpoint with the access token in the header of the request
  - You can use [modheader](https://chromewebstore.google.com/detail/idgpnmonknjnojddfkpgkljpfnnfcklj) to add the header to the request
  - Be sure to add JWT in front of the token, ex: `JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0IiwiZXhwIjoxNjA`
- Permissions -> always add permissions to groups not ad hoc per user otherwise it gets really hard to see who has what permissions

## Recommendations
- Only use SQLite for development


## Cool Resources
- Generating Data -> https://mockaroo.com/
