from flask import request,make_response,jsonify
from flask_restful import Resource, reqparse ,abort
import json
import os
from os import listdir
from os.path import isfile, join
import glob
from app import config
import jwt

class AccountResource(Resource):
    def post(self):
        """
        Create account
        ---
        tags: 
            - User
        parameters:
            - in: body
              name: attribute
              description : user 
              schema: 
                type: object
                properties: 
                    user: 
                        type: string
                    pwd:
                        type: string
        responses:
            201:
                description: Account created
            400: 
                description: Error unkonw , Bad token
            401: 
                description: Account already existant
        """


        body_parser = reqparse.RequestParser()
        body_parser.add_argument('user', type=str, required=True, help='Missing the login of the user')
        body_parser.add_argument('pwd',  type=str, required=True, help='Missing the password associated to the user login')
        args = body_parser.parse_args(strict=True)
        user = args['user']
        pwd  = args['pwd']
        try:
          
            
            with open("app/resources/users.json","r") as jsonFile:
                liste=json.load(jsonFile)
                print(liste)

            print()
            for elt in liste:
                print(elt)
                if(user == elt['user'] and pwd == elt['pwd']):
                    responseObject = {
                    'status': "Failure",
                    'message': 'Compte déjà existant',
     
                    }
                    return make_response(jsonify(responseObject),401)
            print("ezzaeaz")
            liste.append({'user': user, 'pwd': pwd})
            print(liste)
            with open("app/resources/users.json","w") as jsonFile:
                json.dump(liste, jsonFile, indent=4)
           
            
            if not os.path.exists('app/resources/BDD/' + user):
                os.makedirs('app/resources/BDD/' + user)


            responseObject = {
                'status': "Success",
                'message': 'Compte créé',
     
            }
            return make_response(jsonify(responseObject),201)
        except Exception as e:
            print(e)
            abort(400)





