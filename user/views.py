from django.contrib.auth import user_logged_out
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.models import User, Country, City
from user.permissions import IsAnonymous, IsOwner
from user.serializers import AuthSerializer, UserSerializer, CountrySerializer


class AuthView(GenericAPIView):
    """
    #Authentication endpoint.#
    *Returns token if credentials provided are valid*

    **POST request example:**

        * /api/v1/login

            {
                "email": "admin@admin.com",
                "password": "admin@123",
            }

    **Response example:**

        {
            "token":"25c5c4bcc7a667d910548f3d601f4da5696b2801",
            "user_id":1
        }

    ## Fields legend: ##

        * email - string (required)
        * password - string (required)
    """

    permission_classes = [IsAnonymous]
    serializer_class = AuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        raise serializers.ValidationError(serializer.errors)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        # Logout ENDPOINT #
        ** NOTE ** Send GET request with auth token.
        **NOTE** Wih this request, old token will be deleted.
        So, You'll have to login again to get a new token.
        :param request:
        :return: 200 ok
        """
        request._auth.delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )

        return Response({"details": "You are Logged Out"}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """
    #User CRUD endpoint#
    **Endpoint to Create, Retrieve, Update, Destroy user instance.**

    **POST (Create): /api/v1/users **

        {
          "username": "admin",
          "email": "admin@admin.com",
          "first_name": "admin",
          "last_name": "admin"
          "gender": "male",
          "age": 24,
          "country": 1,
          "city": 1,
          "password": "admin@123",
          "confirm_password": "admin@123"
        }

    **GET (Retrieve): /api/v1/users/1**

        {
          "id": 4,
          "username": "admin",
          "first_name": "admin",
          "last_name": "admin",
          "email": "admin@admin.com",
          "gender": "male",
          "age": 24,
          "country": 1,
          "city": 1
        }

    **PUT (Update all fields): /api/v1/users/1**

        {
          "username": "admin",
          "first_name": "abc",
          "last_name": "abc",
          "email": "admin@admin.com",
          "gender": "male",
          "age": 24,
          "country": 1,
          "city": 1
          "password": "abc12345",
          "confirm_password": "abc12345",
          "current_password": "abc1234567"
        }

    **PATCH (Partial update): /api/v1/users/1**

        {
          "username": "string"
        }

    ** PATCH for Password Change : **

        {
          "current_password": "string",
          "password": "string"
        }

    ## Fields Legend: ##

        * username - "string"
        * current_password - "string" <- required when user wants to change the email or password
        * password - "string" <- require when user wants to register and change password
        * email - "string"
        * first_name - "string"
        * last_name - "string"
        * gender - "string"
            -> choices: male - Male, female - Female
        * age - integer
        * country - Primary Key of country
        * city - primary key of city
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def list(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            queryset = self.get_queryset().filter(pk=request.user.id)
            queryset = self.filter_queryset(queryset=queryset)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response([])


class RetrieveCountryCityView(APIView):
    """
    #Country Data endpoint.#

    **GET request example:**

        * /api/v1/country_data

            [
                {
                    "id": 7,
                    "name": "France",
                    "cities":[
                        {
                            "id": 8,
                            "name": "PARIS"
                        },
                        {
                            "id": 46,
                            "name": "Marseille"
                        }
                    ]
                },
            ]
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        countries = Country.objects.all()
        serializer = CountrySerializer(instance=countries, many=True)
        return Response(data=serializer.data)
