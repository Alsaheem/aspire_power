from character.serializers import CharacterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Character, Quote
import requests

# Create your views here.
class HomeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
            {"message": "Welcome to the Character API!"}, status=status.HTTP_200_OK
        )


class ListAllCharaters(APIView):
    # get all characters from the one-dev-api and cascade to /characters
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            api_response = requests.get(
                f"{settings.API_BASE_URL}/character",
                headers={"Authorization": f"Bearer {settings.API_KEY}"},
            )
            if api_response.status_code == 200:
                return Response(api_response.json()["docs"], status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Something went wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListSpecificCharaterQuotes(APIView):
    # list specific character and their quotes
    permission_classes = (AllowAny,)

    def get(self, request, character_id):
        try:
            api_response = requests.get(
                f"{settings.API_BASE_URL}/character/{character_id}/quote",
                headers={"Authorization": f"Bearer {settings.API_KEY}"},
            )
            if api_response.status_code == 200:
                return Response(api_response.json()["docs"], status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "invalid character id"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            return Response(
                {"error": "an error occoured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FavoriteSpecificCharater(APIView):
    # favoriite a character from the one-dev-api and cascade to /characters/:id/favorite
    permission_classes = (IsAuthenticated,)

    def post(self, request, character_id):
        try:
            api_response = requests.get(
                f"{settings.API_BASE_URL}/character/{character_id}",
                headers={"Authorization": f"Bearer {settings.API_KEY}"},
            )

            character = None
            if api_response.status_code == 200:
                for result in api_response.json()["docs"]:
                    if result["_id"] == character_id:
                        character, created = Character.objects.get_or_create(
                            id=result["_id"],
                            name=result["name"],
                            race=result["race"],
                            gender=result["gender"],
                            spouse=result["spouse"],
                            wiki_url=result["wikiUrl"],
                            user=request.user,
                        )
                character_data = CharacterSerializer(character)
                return Response(
                    {"data": character_data.data, "message": "created_successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "invalid character id"}, status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UnFavoriteSpecificCharater(APIView):
    # unfavorite a specific character
    permission_classes = (IsAuthenticated,)

    def post(self, request, character_id):
        try:
            api_response = requests.get(
                f"{settings.API_BASE_URL}/character/{character_id}",
                headers={"Authorization": f"Bearer {settings.API_KEY}"},
            )
            if api_response.status_code == 200:
                for result in api_response.json()["docs"]:
                    if (
                        result["_id"] == character_id
                        and Character.objects.filter(
                            id=result["_id"], user=request.user
                        ).exists()
                    ):
                        character = Character.objects.get(id=result["_id"])
                        character.is_favorite = False
                        character.save()
                    else:
                        return Response(
                            {
                                "error": f"character_id {character_id} is not a favorited character"
                            },
                            status=status.HTTP_404_NOT_FOUND,
                        )
                character_data = CharacterSerializer(character)
                return Response(
                    {
                        "data": character_data.data,
                        "message": f"character {character_id} removed from favorites",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "invalid character id"}, status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": "an error occoured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FavoriteSpecificCharaterAndQuote(APIView):
    # favorite a specific quote from a specific character
    permission_classes = (IsAuthenticated,)

    def post(self, request, character_id, quote_id):
        try:
            character_api_response = requests.get(
                f"{settings.API_BASE_URL}/character/{character_id}",
                headers={"Authorization": f"Bearer {settings.API_KEY}"},
            )
            quote_api_response = requests.get(
                f"{settings.API_BASE_URL}/quote/{quote_id}",
                headers={"Authorization": f"Bearer {settings.API_KEY}"},
            )
            character = None
            if (
                character_api_response.status_code == 200
                and quote_api_response.status_code == 200
            ):
                for result in character_api_response.json()["docs"]:
                    if result["_id"] == character_id:
                        character, created = Character.objects.get_or_create(
                            id=result["_id"],
                            name=result["name"],
                            race=result["race"],
                            gender=result["gender"],
                            spouse=result["spouse"],
                            wiki_url=result["wikiUrl"],
                            user=request.user,
                        )
                        quote_result = quote_api_response.json()["docs"][0]
                        quote, created = Quote.objects.get_or_create(
                            id=quote_result["_id"],
                            dialog=quote_result["dialog"],
                            movie=quote_result["movie"],
                            character=character,
                        )
                character_data = CharacterSerializer(character)
                return Response(character_data.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "invalid character or quote id"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListFavoritedCharaterAndQuotes(APIView):
    # list all user favorited characters and their quotes
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            character = Character.objects.filter(is_favorite=True, user=request.user)
            character_data = CharacterSerializer(character, many=True)
            return Response(character_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
