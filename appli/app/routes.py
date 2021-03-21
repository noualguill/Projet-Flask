from app import api

from app.resources.login import LoginResource
from app.resources.account import AccountResource
from app.resources.lists import ListsResource
from app.resources.lists import ListIdResource
from app.resources.todos import TodosResource
from app.resources.todos import TodosIdResource


# Account
api.add_resource(AccountResource, '/account')

# Login
api.add_resource(LoginResource, '/login')

# Todos app
api.add_resource(ListsResource, '/lists')
api.add_resource(ListIdResource, '/lists/<int:id_list>')
api.add_resource(TodosResource, '/lists/todos/<int:id_list>')
api.add_resource(TodosIdResource, '/lists/todos/<int:id_list>/<int:id_todo>')

