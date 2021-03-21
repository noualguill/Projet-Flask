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




class ListsResource(Resource):
   
    def get(self):
        """
        Get all todolist
        ---
        tags: 
            - GET + CRUD sur Todolist
        parameters:
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing got all todolist
            400: 
                description: Error unkonw , Bad token
        """
        try:
            token = request.headers.get('token')
        
            #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
            auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
            onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
            print(onlyfiles)
            listFinal=[]
            for elt in onlyfiles:
                with open("app/resources/BDD/"+auth_token+"/"+elt,"r") as jsonFile:
                    liste=json.load(jsonFile)
                listFinal.append(liste)
            responseObject = {
            'status': 'Success',
            'message': 'Toutes les listes de Todos de l\'utilisateur '+auth_token,
            'data': listFinal
            }
            return make_response(jsonify(responseObject),201)
        except Exception as e:
            print(e)
            abort(400)


    def put(self):
        """
        Add a todolist
        ---
        tags: 
            - GET + CRUD sur Todolist
        parameters:
            - in: body
              name: attribute
              description : The name of the todolist
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing added todolist
            400: 
                description: Error unkonw , Bad token
            404:
                description: The list does not exist
        """
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('name',type=str,required=True, help="Il manque le nom de la TodoList")

        args= body_parser.parse_args(strict=True)
        print("aezazeza")
        try:
            name = args['name']
      
            return creaTodoList(name)
        except Exception as e:
            print(e)
            raise(e)


def creaTodoList(name):
    
    token = request.headers.get('token')
    #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
    auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
    onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
    l_index= []
    print(onlyfiles)

    accFinal=-1
    for e in onlyfiles:
        l_index.append(e.split("_")[0])
    print(l_index)
    if (len(l_index)==0):
        accFinal=0
        print("rzerze")
    else:
        l_index_int = [int(i) for i in l_index]
        print("zerze")
        print(l_index_int)
        missingNumbers = [ i  for i in range(len(l_index_int)) if i not in l_index_int ]
        print(missingNumbers)


        if (len(missingNumbers)>0):
            accFinal=missingNumbers[0]
        elif (len(missingNumbers)==0):
            accFinal= l_index_int[-1]+1

    countFiles = len(onlyfiles)

    if (name+".json" in onlyfiles):
        responseObject = {
            'status': 'Failure',
            'message': 'Nom de TodoList déjà existant',
        }        
        return make_response(jsonify(responseObject),404)
    else:
        print(accFinal)
        with open("app/resources/BDD/"+auth_token+"/"+str(accFinal)+"_"+name+".json","w+") as f:
          
            liste=[]
    
            liste.append({"id_list":accFinal,"name":name,"todos":[]})
            json.dump(liste,f,indent=4)
        
        responseObject = {
            'status': 'Success',
            'message': 'Ajout ListTodo',
            
        }
        return make_response(jsonify(responseObject),201)






class ListIdResource(Resource):

    def get(self,id_list):
        """
        Get a todos from a todolist
        ---
        tags: 
            - GET + CRUD sur Todolist
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
            res=""
            for elt in onlyfiles:
        
                if (elt.lstrip('_')[0]==str(id_list)):
                    res= elt

        
            print(res)
            if (res!=""):
                with open("app/resources/BDD/"+auth_token+"/"+res,"r") as jsonFile:
                    liste=json.load(jsonFile)
                print(liste[0]['todos'])
                responseObject = {
                'status': 'Success',
                'message': 'Requete Get effectuée',
                'data': liste
                }
                return make_response(jsonify(responseObject),201)
            else:
                responseObject = {
                'status': 'Failure',
                'message': 'Cet Id de TodoList n\'existe pas',
               
                }
                return make_response(jsonify(responseObject),404)
        except Exception as e:
            print(e)
            abort(400)



    def delete(self,id_list):
        """
        Delete a todolist
        ---
        tags: 
            - GET + CRUD sur Todolist
        parameters:
            - in: path
              name: id_list
              description: The id of the list to edit
              required: true
              type: string
            - in : header
              name: token
              description : user authentication token
              type: string
              required : true
        responses:
            201:
                description: JSON representing deleted todolist
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
         
            res=""
            for elt in onlyfiles:
        
                if (elt.lstrip('_')[0]==str(id_list)):
                    res= elt

            
            print(res)
            if (res!=""):
                os.remove("app/resources/BDD/"+auth_token+"/"+res)
                responseObject = {
                'status': 'Success',
                'message': 'Fichier '+res+' supprimé',
               
                }
                return make_response(jsonify(responseObject),201)
            else:
                responseObject = {
                'status': 'Failure',
                'message': 'Fichier non supprimé car l\'id ne correspond à aucun fichier',
               
                }
                return make_response(jsonify(responseObject),404)

        except Exception as e:
            print(e)
            abort(400)



    def patch(self,id_list):
        """
        Edit a todolist
        ---
        tags: 
            - GET + CRUD sur Todolist
        parameters:
            - in: path
              name: id_list
              description: The id of the list to edit
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
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('name',type=str,required=True, help="Il manque le nom de la TodoList")
        token = request.headers.get('token')
        args= body_parser.parse_args(strict=True)
        print("aezazeza")
        try:
            name = args['name']
            print("qdqsd")
            return modif(name,token,id_list)
        except Exception as e:
            print(e)
            abort(400)

def modif(name,token,id_list):
        
            
    token = request.headers.get('token')
    #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidG90byJ9.-iDY84XrUUuu32T8NKJY3HBIoQnHRfoZQEpwEyiiX6o"
    auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('user')
    onlyfiles = [f for f in listdir("app/resources/BDD/"+auth_token+"/") if isfile(join("app/resources/BDD/"+auth_token+"/", f))]
    print(onlyfiles)
    res=""
    for elt in onlyfiles:
        print(id_list)
        print(elt.lstrip('_')[0]==str(id_list))
        if (elt.lstrip('_')[0]==str(id_list)):
            res= elt


    
    print(res)
    if (res!=""):
        with open("app/resources/BDD/"+auth_token+"/"+res,"r") as jsonFile:
            liste=json.load(jsonFile)
        print("toto")
        liste[0]['name']=name

        with open("app/resources/BDD/"+auth_token+"/"+res, "w") as jsonFile:
            json.dump(liste, jsonFile,indent=4)
        responseObject = {
        'status': 'Success',
        'message': 'Fichier '+res+' patché',
        'data':liste
        
        }
        return make_response(jsonify(responseObject),202)
    else:
        responseObject = {
        'status': 'Failure',
        'message': 'Fichier non patché car l\'id ne correspond à aucun fichier',
        
        }
        return make_response(jsonify(responseObject),404)






