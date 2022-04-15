from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getTest(request):
    person = 'API Active'
    return Response(person)

@api_view(['GET'])
def getCharacter(request):
    return Response('nah')