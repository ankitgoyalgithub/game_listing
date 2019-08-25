import base64
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from games.models import Game

class PublicEndpoint(permissions.BasePermission):
	def has_permission(self, request, view):
		return True

class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            encodedcredentials = request.data.get('credentials')
            decodedcredentials = base64.b64decode(encodedcredentials).decode('ascii')
            username, password = decodedcredentials.split(':')
            tempdict = {'username':username, 'password':password}
            serializer = self.serializer_class(data=tempdict)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id':user.id, 'username':user.username, 'email': user.email, 'firstname':user.first_name, 'lastname':user.last_name})
        except Exception as e:
            raise e

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def upload(request):
    try:
        if (not request.FILES) and (not("game_details" in request.FILES)) :
            raise APIException(detail="No Files Uploaded", status=status.HTTP_400_BAD_REQUEST)  
        else:
            game_details_file = request.FILES["game_details"]
            
            header = []

            for line in game_details_file.readlines():
                line = line.decode().split(',')

                if len(header) == 0:
                    header = line
                else:
                    title = line[0]
                    platform = line[1]
                    score = float(line[2])
                    genre = line[3]
                    editors_choice = True if line[4] == 'Y' else False

                    g = Game(title=title, platform=platform, score=score, genre=genre, editors_choice=editors_choice)
                    g.save()

            return HttpResponse(json.dumps({'success':'File Successfully Uploaded'}),content_type='application/json', status=200)
    except Exception as e:
        raise e		

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def search(request):
    try:
        if not ('q' in request.GET):
            raise APIException(detail="No Search Parameter", status=status.HTTP_400_BAD_REQUEST)
        else:
            query_parameter = request.GET['q']
            query_parameter = query_parameter.split(' ')
            search_result = dict()

            for words in query_parameter:
                result = Game.objects.filter(title__contains=words)

                for game in result:
                    if game.id not in search_result:
                        search_result[game.id] = {
                            "title": game.title,
                            "platform": game.platform,
                            "score": float(game.score),
                            "genre": game.genre,
                            "editors_choice": "Y" if game.editors_choice == 1 else "N"
                        }
            return HttpResponse(json.dumps({"results":search_result}),content_type='application/json', status=200)
    except Exception as e:
        raise e
