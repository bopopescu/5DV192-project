from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from user.serializers import UserSerializer
from user.validators import is_empty_json
from user.functions import generate_hash, decode_request_body
from django.views import View as APIView
import json
from django.core.serializers.json import DjangoJSONEncoder

from user.models import User, UserSession




class UserRegisterView(APIView):

    def get(self, request, *args, **kwargs):

        return JsonResponse({
            'errors': "asd"
        }, status=201)

    def post(self, request, *args, **kwargs):

        data = decode_request_body(request)

        errors = self.validate(data)

        password = data["password"]
        username = data["username"]

        print(" ")
        print(data)

        if is_empty_json(errors):

            session_key = generate_hash(256)
            hashed_password = make_password(password)

            print("registration successful")
            print("session: " + session_key)
            print("hashed password: " + hashed_password)
            print("match?: " + str(check_password(password, hashed_password)))

            try:

                user = User.objects.create(username=username, password=hashed_password)
                UserSession.objects.create(user=user, session_key=session_key)

                return JsonResponse({
                    'sessionKey': session_key,
                }, status=200)

            except Exception:

                errors["nonFieldError"] = "This username already exists"

                return JsonResponse({
                    'errors': errors
                }, status=400)

        else:

            print("registration failed")
            print(errors)

            return JsonResponse({
                'errors': errors
            }, status=400)

    def validate(self, data):

        errors = {}

        username = data["username"]
        password = data["password"]
        password2 = data["password2"]

        print("username: " + username)
        print("password1: " + password)
        print("password2: " + password2)

        # check for errors

        if len(username) < 3:
            errors["username"] = "Username is too short"
        if len(username) > 32:
            errors["username"] = "Username is too long"

        if password != password2:
            errors["password1"] = "Passwords does not match"
        if len(password) < 6:
            errors["password1"] = "Password is too short"
        if len(password) > 1024:
            errors["password1"] = "Password is too long"

        return errors


class UserLoginView(APIView):

    def get(self, request, *args, **kwargs):

        print(request)

        return JsonResponse({
            'errors': "login test"
        }, status=201)


    def post(self, request, *args, **kwargs):

        data = decode_request_body(request)

        print(" ")
        print(data)

        username = data["username"]

        errors = self.validate(data)

        if is_empty_json(errors):

            session_key = generate_hash(256)
            user = User.objects.get(username=username)
            UserSession.objects.create(user=user, session_key=session_key)

            print("UserLoginView: success")

            return JsonResponse({
                'sessionKey': session_key,
            }, safe=False, status=200)

        else:

            print("UserLoginView: fail")
            print(errors)

            return JsonResponse({
                'errors': errors
            }, status=400)

    def validate(self, data):

        errors = {}

        username = data["username"]
        password = data["password"]

        print("username: " + username)
        print("password: " + password)

        # check for errors

        if not User.objects.filter(username=username).exists():
            errors["nonFieldError"] = "This account does not exist"

        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).values('password')
            user_password = user[0]['password']
            if not check_password(password, user_password):
                errors["nonFieldError"] = "Invalid password"

        return errors


class UserLogoutView(APIView):

    def post(self, request, *args, **kwargs):

        data = decode_request_body(request)

        print(" ")
        print(data)

        session_key = data["sessionKey"]
        print(session_key)

        try:
            session = UserSession.objects.filter(session_key=session_key)
            session.delete()
        except ObjectDoesNotExist:
            return JsonResponse({
                'errors': 'Invalid session key.'
            }, status=400)

        return JsonResponse({
            'response': 'Session terminated'
        }, status=200)


class UserGetView(APIView):

    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        session_key = self.kwargs.get('key')

        print(session_key)

        if UserSession.objects.filter(session_key=session_key).exists():

            sessions = UserSession.objects.filter(session_key=session_key).values('user')
            print("sessions")
            print(sessions)
            user_id = sessions[0]['user']
            users = User.objects.filter(id=user_id).values('date_registered', 'username', 'coins')
            user = users[0]

            user_json = {
                'dateRegistered': user.get('date_registered'),
                'username': user.get('username'),
                'coins': user.get('coins'),
            }

        else:

            return JsonResponse({
                'errors': 'invalid session'
            }, status=400)

        return JsonResponse(user_json, safe=False, status=200)


class UserSetCoinsView(APIView):

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        data = decode_request_body(request)

        print(" ")
        print(data)

        coins = data["coins"]
        session_key = data["sessionKey"]

        if UserSession.objects.filter(session_key=session_key).exists():

            sessions = UserSession.objects.filter(session_key=session_key).values('user')
            print("sessions")
            print(sessions)
            user_id = sessions[0]['user']

            obj = User.objects.get(id=user_id)
            obj.coins = coins
            obj.save()

            return JsonResponse({}, safe=False, status=200)

        else:

            return JsonResponse({
                'errors': 'invalid user session'
            }, status=400)


class UserGetUsersView(APIView):

    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        users = json.dumps([dict(item) for item in User.objects.all().values('username', 'coins')])

        response = {
            'users': users
        }

        return JsonResponse(response, safe=False, status=200)
