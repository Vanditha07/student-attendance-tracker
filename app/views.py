
import pyrebase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer, SubjectInSerializer, SubjectDisplaySerializer,  AddClassSerializer
from rest_framework.authtoken.models import Token
from .attendance import Attendance
import json
from .extras import JSONfile

firebaseConfig = {
  'apiKey': "AIzaSyAXyx22l2RMTUHwMGJdPnURux2kRw1e-CM",
  'authDomain': "attendance-tracker-b1cfc.firebaseapp.com",
  'databaseURL': "https://attendance-tracker-b1cfc-default-rtdb.firebaseio.com",
  'projectId': "attendance-tracker-b1cfc",
  'storageBucket': "attendance-tracker-b1cfc.appspot.com",
  'messagingSenderId': "185262330326",
  'appId': "1:185262330326:web:d05944a7a9d36c64ce1477"
};

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
fb_db = firebase.database()

@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            fb_db.child('User').push(account.email)           
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data)


@api_view(['POST', ])
def add_subject_view(request):
    
    if request.method == 'POST':
        serializer = SubjectInSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            details = serializer.save()
            email = details.email
            subject = details.subject

            fb_db.child(email).push(subject)

@api_view(['GET', ])
def data_display_view(request, username):

    if request.method == 'GET':
        output = {}
        result = fb_db.get('Users/', None)

        for k, value in result.items():    #email and dict
            if k == username:
                for i, j in value.items():     #subject and dict
                    absent = 0 
                    present = 0
                    for m, n in j.items():     #date and dict

                        for a, b in n.items(): #loop over present and absent
                            if m == 'A':
                                absent = absent + value  
                            if m == 'P':
                                present = present + value 

                    total = present + absent 
                    percentage = Attendance(present, absent, total)
                    
                    output.add(j, percentage)
            
        upload = json.dumps(output)
        object = JSONfile(upload)
        serializer_class = SubjectDisplaySerializer(object)
        return Response(serializer_class.data)

@api_view(['POST, '])
def data_display_view(request, username, classname):
    if request.method == 'POST':
        serializer =  AddClassSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            details = serializer.save()
            date = details.date
            absent = details.absent
            present = details.present

            result = fb_db.get('Users/', None)
            for k, value in result.items():    #email and dict
                if k == username:
                    for i, j in value.items():
                        if i == classname:
                            j.add(
                                {
                                    date : 
                                    {
                                        'A': absent,
                                        'P': present
                                    }
                        
                                })
            data['response'] = 'successfully added new value.'
            return Response(data)  













        
		