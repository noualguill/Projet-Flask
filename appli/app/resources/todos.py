from flask import request,make_response,jsonify
from flask_restful import Resource, reqparse ,abort
import json
import os
from os import listdir
from os.path import isfile, join
import glob
from app import config
import jwt

from datetime import datetime

# datetime object containing current date and time


now = str(datetime.now())




class TodosResource(Resource):

    def get(self,id_list):
        """
        Get a todos from a todolist
        ---
        tags: 
            - GET + CRUD sur Todo
        parameters:
            - in: path
              name: id_list
              description: The id of the list to get
              required: true
              type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing got todolist
            400: 
                description: Error unkonw , Bad token
            404:
                description: The list does not exist
        """
        try:
            token = request.headers.get('token')
        
            #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
            auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
            onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
            print(onlyfiles)
            listFinal=[]
        
            elt=""
           
   
           
            for e in onlyfiles:
                stock=e.split("_")
                if (id_list == int(stock[0])):
                    elt=e
                
            if (elt==""):
                responseObject = {
                'status': 'Failure',
                'message': 'Id liste Todos faux '
  
                }
                return make_response(jsonify(responseObject),404)
            else:
                
                with open("app/resources/BDD/"+auth_token+"/"+elt,"r") as jsonFile:
                    liste=json.load(jsonFile)
               
                responseObject = {
                'status': 'Success',
                'message': 'Toutes les listes de Todos de l\'utilisateur '+auth_token,
                'data': liste[0]
                }
                return make_response(jsonify(responseObject),201)
        except Exception as e:
            print(e)
            abort(400)   

    def put(self,id_list):
        """
        Add a todo
        ---
        tags: 
            - GET + CRUD sur Todo
        parameters:
            - in: path
              name: id_list
              description: The id of the list to add
              required: true
              type: string
            - in: body
              name: attribute
              description : The name of the todo
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
                    content:
                        type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing added todo
            400: 
                description: Error unkonw , Bad token
            404:
                description: Not Found
        """
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('name',type=str,required=True, help="Il manque le nom du Todo")
        body_parser.add_argument('content',type=str,required=True, help="Il manque le content du Todo")

        args= body_parser.parse_args(strict=True)
        print("aezazeza")
        try:
            name = args['name']
            content = args['content']
      
            return creaTodoList(name,content,id_list)
        except Exception as e:
            print(e)
            raise(e)


def creaTodoList(name,content,id_list):
    
    token = request.headers.get('token')
    #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
    auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
    onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
   
    print(onlyfiles)
    l_index= []
    listFinal=[]

    elt=""



    for e in onlyfiles:
        stock=e.split("_")
        print(id_list)
        print(stock[0])
        if (id_list == int(stock[0])):
            elt=e
            print(elt)
   
    if (elt==""):
        responseObject = {
        'status': 'Failure',
        'message': 'Id liste Todos faux '

        }
        return make_response(jsonify(responseObject),404)
    else:
        print("app/resources/BDD/"+auth_token+"/"+elt)
        with open("app/resources/BDD/"+auth_token+"/"+elt,"r") as jsonFile:
            liste=json.load(jsonFile)
        print("azeaze")
        print(liste[0]['todos'])
        l_index_todo=[]
        for i in liste[0]['todos']:
            l_index_todo.append(i['id_todo'])
        print(l_index_todo)

        accFinal=-1
        if (len(l_index_todo)==0):
            accFinal=0
            print("rzerze")
        else:
      
            print("zerze")
          
            missingNumbers = [ i  for i in range(len(l_index_todo)) if i not in l_index_todo ]
            print(missingNumbers)


            if (len(missingNumbers)>0):
                accFinal=missingNumbers[0]
            elif (len(missingNumbers)==0):
                accFinal=max(l_index_todo)+1
            else:
                accFinal= max(missingNumbers)+1


        print(accFinal)
        with open("app/resources/BDD/"+auth_token+"/"+elt,"w+") as f:
            print(name +" "+ content)
    

            liste[0]['todos'].append({"id_todo":accFinal,"name":name,"content":content,"last_modified":now})
            print(liste)
            json.dump(liste,f,indent=4)
        
        responseObject = {
            'status': 'Success',
            'message': 'Ajout Todo',
            
        }
        return make_response(jsonify(responseObject),201)


class TodosIdResource(Resource):


    def get(self,id_list,id_todo):
        """
        Get a todos from a todolist
        ---
        tags: 
            - GET + CRUD sur Todo
        parameters:
            - in: path
              name: id_list
              description: The id of the list to get
              required: true
              type: string
            - in: path
              name: id_todo
              description: The id of the todo to get
              required: true
              type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing got todolist
            400: 
                description: Error unkonw , Bad token
            404:
                description: The list does not exist
        """
        try:
            token = request.headers.get('token')
        
            #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
            auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
            onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
            print(onlyfiles)
            listFinal=[]
        
            elt=""
            acc=0
            accFinal=-1
           
            for e in onlyfiles:
                stock=e.split("_")
                if (id_list == int(stock[0])):
                    elt=e
                
            if (elt==""):
                responseObject = {
                'status': 'Failure',
                'message': 'Id liste Todos faux '
  
                }
                return make_response(jsonify(responseObject),404)
            else:
                
                with open("app/resources/BDD/"+auth_token+"/"+elt,"r") as jsonFile:
                    liste=json.load(jsonFile)
                
                print(liste[0]['todos'])
                for i in liste[0]['todos']:
                    if (i["id_todo"]==id_todo):
                        accFinal=acc
                    acc=acc+1
                if (accFinal==-1):
                    responseObject = {
                    'status': 'Failure',
                    'message': 'ID Todo Faux'
                    }
                    return make_response(jsonify(responseObject),404)                    
                else:
                    responseObject = {
                    'status': 'Success',
                    'message': 'Todo bien récupéré ',
                    'data': liste[0]['todos'][accFinal]
                    }
                    return make_response(jsonify(responseObject),201)
        except Exception as e:
            print(e)
            abort(400) 


    def delete(self,id_list,id_todo):
        """
        Add a todo
        ---
        tags: 
            - GET + CRUD sur Todo
        parameters:
            - in: path
              name: id_list
              description: The id of the list to delete
              required: true
              type: string
            - in: path
              name: id_todo
              description: The id of the todo to delete
              required: true
              type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing deleted todo
            400: 
                description: Error unkonw , Bad token
            404:
                description: Not Found
        """
        try:
            token = request.headers.get('token')
        
            #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
            auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
            onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
            print(onlyfiles)
            listFinal=[]
        
            elt=""
            acc=0
            accFinal=-1
           
            for e in onlyfiles:
                stock=e.split("_")
                if (id_list == int(stock[0])):
                    elt=e
                
            if (elt==""):
                responseObject = {
                'status': 'Failure',
                'message': 'Id liste Todos faux '
  
                }
                return make_response(jsonify(responseObject),404)
            else:
                
                with open("app/resources/BDD/"+auth_token+"/"+elt,"r") as jsonFile:
                    liste=json.load(jsonFile)
                
                print(liste[0]['todos'])
                for i in liste[0]['todos']:
                    if (i["id_todo"]==id_todo):
                        accFinal=acc
                    acc=acc+1
                if (accFinal==-1):
                    responseObject = {
                    'status': 'Failure',
                    'message': 'ID Todo Faux'
                    }
                    return make_response(jsonify(responseObject),404)                    
                else:
                    print("tozotze")
                    del liste[0]['todos'][accFinal]
                    print(liste)
                    print("app/resources/BDD/"+auth_token+"/"+elt)
                    with open("app/resources/BDD/"+auth_token+"/"+elt,"w+") as jsonFile:
                        json.dump(liste,jsonFile,indent=4)
             
                    responseObject = {
                    'status': 'Success',
                    'message': 'Todo bien supprimé ',
                    'data': liste
                    }
                    return make_response(jsonify(responseObject),201)
        except Exception as e:
            print(e)
            abort(400) 


    def patch(self,id_list,id_todo):
        """
        Edit a todolist
        ---
        tags: 
            - GET + CRUD sur Todo
        parameters:
            - in: path
              name: id_list
              description: The id of the list to edit
              required: true
              type: string
            - in: path
              name: id_todo
              description: The id of the todo to edit
              required: true
              type: string
            - in: body
              name: attribute
              description : The edited name of the todolist
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
                    content:
                        type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            202:
                description: JSON representing edited todolist
            400: 
                description: Error unkonw , Bad token
            404:
                description: The list does not exist
        """
        try:
            body_parser = reqparse.RequestParser()
            body_parser.add_argument('name',type=str,required=True, help="Il manque le nom du Todo")
            body_parser.add_argument('content',type=str,required=True, help="Il manque le content du Todo")
            token = request.headers.get('token')
            args= body_parser.parse_args(strict=True)
            name = args['name']
            content = args['content']
            #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
            auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
            onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
            print(onlyfiles)
            listFinal=[]
        
            elt=""
            acc=0
            accFinal=-1
           
            for e in onlyfiles:
                stock=e.split("_")
                if (id_list == int(stock[0])):
                    elt=e
                
            if (elt==""):
                responseObject = {
                'status': 'Failure',
                'message': 'Id liste Todos faux '
  
                }
                return make_response(jsonify(responseObject),404)
            else:
                
                with open("app/resources/BDD/"+auth_token+"/"+elt,"r") as jsonFile:
                    liste=json.load(jsonFile)
                
                print(liste[0]['todos'])
                for i in liste[0]['todos']:
                    if (i["id_todo"]==id_todo):
                        accFinal=acc
                    acc=acc+1
                if (accFinal==-1):
                    responseObject = {
                    'status': 'Failure',
                    'message': 'ID Todo Faux'
                    }
                    return make_response(jsonify(responseObject),404)                    
                else:
                    print("tozotze")
                    liste[0]['todos'][accFinal]['name'] = name
                    liste[0]['todos'][accFinal]['content'] = content
                    liste[0]['todos'][accFinal]['last_modified'] = now
                    print(liste)
                    print("app/resources/BDD/"+auth_token+"/"+elt)
                    with open("app/resources/BDD/"+auth_token+"/"+elt,"w+") as jsonFile:
                        json.dump(liste,jsonFile,indent=4)
             
                    responseObject = {
                    'status': 'Success',
                    'message': 'Todo bien supprimé ',
                    'data': liste
                    }
                    return make_response(jsonify(responseObject),202)
        except Exception as e:
            print(e)
            abort(400) 
