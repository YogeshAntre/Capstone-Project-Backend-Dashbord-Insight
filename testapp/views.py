
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Count, F, Q,Max
from .models import Match, Player, Batting, Bowling
from .serializers import MatchSerializer, PlayerSerializer, BattingSerializer, BowlingSerializer
from .pagination import DefaultPagination

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('-match_date')
    serializer_class = MatchSerializer
    pagination_class = DefaultPagination
    
    @action(detail=False, methods=['get'])
    def team_matches(self, request):
        team_name = request.query_params.get('team')
        if team_name:
            matches = Match.objects.filter(Q(team1=team_name) | Q(team2=team_name)).order_by('-match_date')
            page = self.paginate_queryset(matches)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(matches, many=True)
            return Response(serializer.data)
        return Response({"error": "Team name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def ground_matches(self, request):
        ground_name = request.query_params.get('ground')
        if ground_name:
            matches = Match.objects.filter(ground=ground_name).order_by('-match_date')
            page = self.paginate_queryset(matches)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(matches, many=True)
            return Response(serializer.data)
        return Response({"error": "Ground name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('name')
    serializer_class = PlayerSerializer
    pagination_class = DefaultPagination
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        player = self.get_object()
        
        # Batting stats
        batting_stats = Batting.objects.filter(player=player).aggregate(
            total_matches=Count('id'),
            total_runs=Sum('runs'),
            total_balls=Sum('balls'),
            total_fours=Sum('fours'),
            total_sixes=Sum('sixes'),
            average=Avg('runs'),
            strike_rate=Avg('strike_rate')
        )
        
        # Bowling stats
        bowling_stats = Bowling.objects.filter(player=player).aggregate(
            total_matches=Count('id'),
            total_wickets=Sum('wickets'),
            total_overs=Sum('overs'),
            total_runs_conceded=Sum('runs_conceded'),
            total_maidens=Sum('maidens'),
            average_economy=Avg('economy')
        )
        
        return Response({
            'player': PlayerSerializer(player).data,
            'batting': batting_stats,
            'bowling': bowling_stats
        })

class BattingViewSet(viewsets.ModelViewSet):
    queryset = Batting.objects.all().order_by('-runs')
    serializer_class = BattingSerializer
    pagination_class = DefaultPagination
    
    @action(detail=False, methods=['get'])
    def top_scorers(self, request):
        limit = int(request.query_params.get('limit', 10))
        top_scorers = Batting.objects.values(
            'player__id', 'player__name'
        ).annotate(
            total_runs=Sum('runs'),
            total_matches=Count('id'),
            average=Avg('runs'),
            strike_rate=Avg('strike_rate')
        ).order_by('-total_runs')[:limit]
        return Response(top_scorers)
    
    @action(detail=False, methods=['get'])
    def by_match(self, request):
        match_id = request.query_params.get('match_id')
        if not match_id:
            return Response({"error": "match_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # First try to find match by match_id field
            batting_records = Batting.objects.filter(match__match_id=match_id).order_by('batting_position')
            if not batting_records.exists():
                # If not found, try by primary key (ID)
                batting_records = Batting.objects.filter(match_id=match_id).order_by('batting_position')
            
            serializer = self.get_serializer(batting_records, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BowlingViewSet(viewsets.ModelViewSet):
    queryset = Bowling.objects.all().order_by('-wickets')
    serializer_class = BowlingSerializer
    pagination_class = DefaultPagination
    
    @action(detail=False, methods=['get'])
    def top_wicket_takers(self, request):
        limit = int(request.query_params.get('limit', 10))
        top_bowlers = Bowling.objects.values(
            'player__id', 'player__name'
        ).annotate(
            total_wickets=Sum('wickets'),
            total_matches=Count('id'),
            average_economy=Avg('economy')
        ).order_by('-total_wickets')[:limit]
        return Response(top_bowlers)
    
    



class PlayerPerformanceView(APIView):
    def get(self, request, player_id):
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get batting performances
        batting_performances = Batting.objects.filter(player=player).select_related('match').order_by('-match__match_date')
        batting_serializer = BattingSerializer(batting_performances, many=True)
        
        # Get bowling performances
        bowling_performances = Bowling.objects.filter(player=player).select_related('match').order_by('-match__match_date')
        bowling_serializer = BowlingSerializer(bowling_performances, many=True)
        
        # Career statistics
        batting_stats = batting_performances.aggregate(
            total_runs=Sum('runs'),
            total_balls=Sum('balls'),
            total_matches=Count('id'),
            average=Avg('runs'),
            strike_rate=Avg('strike_rate'),
            total_fours=Sum('fours'),
            total_sixes=Sum('sixes')
        )
        
        bowling_stats = bowling_performances.aggregate(
            total_wickets=Sum('wickets'),
            total_overs=Sum('overs'),
            total_runs_conceded=Sum('runs_conceded'),
            total_maidens=Sum('maidens'),
            average_economy=Avg('economy')
        )
        
        return Response({
            'player': PlayerSerializer(player).data,
            'batting_performances': batting_serializer.data,
            'bowling_performances': bowling_serializer.data,
            'career_stats': {
                'batting': batting_stats,
                'bowling': bowling_stats
            }
        })

class ComparePlayersView(APIView):
    def get(self, request):
        player_ids = request.query_params.get('ids', '')
        if not player_ids:
            return Response({"error": "Player IDs parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            player_ids = [int(id) for id in player_ids.split(',')]
        except ValueError:
            return Response({"error": "Invalid player IDs format"}, status=status.HTTP_400_BAD_REQUEST)
        
        players_data = []
        for player_id in player_ids:
            try:
                player = Player.objects.get(id=player_id)
            except Player.DoesNotExist:
                continue
                
            # Batting stats
            batting_stats = Batting.objects.filter(player=player).aggregate(
                total_matches=Count('id'),
                total_runs=Sum('runs'),
                total_balls=Sum('balls'),
                total_fours=Sum('fours'),
                total_sixes=Sum('sixes'),
                average=Avg('runs'),
                strike_rate=Avg('strike_rate'),
                highest_score=Max('runs')
            )
            
            # Bowling stats
            bowling_stats = Bowling.objects.filter(player=player).aggregate(
                total_matches=Count('id'),
                total_wickets=Sum('wickets'),
                total_overs=Sum('overs'),
                total_runs_conceded=Sum('runs_conceded'),
                total_maidens=Sum('maidens'),
                average_economy=Avg('economy'),
                best_bowling=Max('wickets')
            )
            
            players_data.append({
                'player': PlayerSerializer(player).data,
                'batting': batting_stats,
                'bowling': bowling_stats
            })
        
        return Response(players_data)