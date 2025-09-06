
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import MatchViewSet, PlayerViewSet, BattingViewSet, BowlingViewSet,PlayerPerformanceView,ComparePlayersView

# router = DefaultRouter()
# router.register(r'matches', MatchViewSet, basename='match')
# router.register(r'players', PlayerViewSet, basename='player')
# router.register(r'batting', BattingViewSet, basename='batting')
# router.register(r'bowling', BowlingViewSet, basename='bowling')
# path("player-performance/<int:player_id>/", PlayerPerformanceView.as_view(), name="player-performance"),
# path("compare-players/", ComparePlayersView.as_view(), name="compare-players"),

# urlpatterns = [
#     path('', include(router.urls)),  # Include DRF router URLs
# ]

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MatchViewSet, 
    PlayerViewSet, 
    BattingViewSet, 
    BowlingViewSet,
    PlayerPerformanceView,
    ComparePlayersView
)

# Create DRF router and register ViewSets
router = DefaultRouter()
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'batting', BattingViewSet, basename='batting')
router.register(r'bowling', BowlingViewSet, basename='bowling')

# Combine router URLs with custom views
urlpatterns = [
    path('', include(router.urls)),
    path('player-performance/<int:player_id>/', PlayerPerformanceView.as_view(), name='player-performance'),
    path('compare-players/', ComparePlayersView.as_view(), name='compare-players'),
]
