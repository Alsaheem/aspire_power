from django.urls import path
from .views import (
    HomeView,
    ListAllCharaters,
    ListSpecificCharaterQuotes,
    FavoriteSpecificCharater,
    UnFavoriteSpecificCharater,
    ListFavoritedCharaterAndQuotes,
    FavoriteSpecificCharaterAndQuote,
)

# app_name = "character"

urlpatterns = [
    # Apis
    path("", HomeView.as_view(), name="home"),
    path("characters/", ListAllCharaters.as_view(), name="characters"),
    path(
        "characters/<str:character_id>/quotes",
        ListSpecificCharaterQuotes.as_view(),
        name="list_character_quotes",
    ),
    path(
        "characters/<str:character_id>/favorites",
        FavoriteSpecificCharater.as_view(),
        name="add_favorite",
    ),
    path(
        "characters/<str:character_id>/favorites/remove",
        UnFavoriteSpecificCharater.as_view(),
        name="remove_favorite",
    ),
    path(
        "characters/<str:character_id>/quotes/<str:quote_id>/favorites",
        FavoriteSpecificCharaterAndQuote.as_view(),
        name="add_favorite_quote",
    ),
    path("favorites/", ListFavoritedCharaterAndQuotes.as_view(), name="favorites"),
]
