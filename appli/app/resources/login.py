from flask import request,make_response,jsonify
from flask_restful import Resource, reqparse ,abort
import json
import os
from os import listdir
from os.path import isfile, join
import glob
from app import config
import jwt

class LoginResource(Resource):
    def post(self):
        """
        Login
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
                description: Good account
            400: 
                description: Error unkonw , Bad token
            404: 
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

         
            for elt in liste:
                print(elt)
                if(user == elt['user'] and pwd == elt['pwd']):
                    encoded = jwt.encode({"user": user},config.API_KEY, algorithm="HS256")
                    responseObject = {
                    'status': "Success",
                    'message': 'Connexion réussie',
                    'data': encoded
                    }
                    return make_response(jsonify(responseObject),201)
    
            responseObject = {
            'status': "Failure",
            'message': 'Compte pas trouvé'

            }
            return make_response(jsonify(responseObject),404)
           
            



        except Exception as e:
            print(e)
            abort(400)





