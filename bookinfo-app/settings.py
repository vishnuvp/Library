import os
schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'title': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 100,
        'required': True,
        'unique': True,
    },
    'author': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 15,
        'required': True,
    },
    # 'role' is a list, and can only contain values from 'allowed'.
    'genre': {
        'type': 'list',
        'allowed': ["Anthology", "Action", "Adventure", "Quest", "Fantasy", "Fiction", "Horror", "Romance", "Satire", "Suspense", "Thriller"],
    },
    
}


books = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'book',
     'additional_lookup': {
        'url': 'regex("[\w\s]+")',
        'field': 'title'
    },
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    # 'resource_methods': ['GET', 'POST','PATCH'],
    # 'item_methods': ['GET', 'POST','PATCH'],
    'schema': schema
}

DOMAIN = {
    'book': books,
}
MONGO_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGODB_PORT', '27017'))

MONGO_DBNAME = 'bookinfo'

# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
