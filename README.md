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
- slug = part of url that is used by search engines
  - ex: `get-max-and-min-formatted-values-from-queryset` part of a stackoverflow question 


## Recommendations
- Only use SQLite for development


## Cool Resources
- Generating Data -> https://mockaroo.com/