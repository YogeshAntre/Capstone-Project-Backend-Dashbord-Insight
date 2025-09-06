from tokenize import TokenError
from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authapp.serializers import UserSerializer

from rest_framework_simplejwt.tokens import UntypedToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
class CustomAuthUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print('YOgesh',serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JWTLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=username,email=email, password=password)
        print('User',user)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class CustomRefreshView(APIView):
   
    def post(self, request):
        refresh_token = request.data.get("refresh")
        print('Refresh Token',refresh_token)
        if not refresh_token:
            return Response({"error": "Refresh token required"})

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)

            return Response({
                "access": new_access
            }, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomVerifyView(APIView):
    """
    Verify if a given token is valid (access or refresh).
    """
    
    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            UntypedToken(token)  # validates signature & expiry
            return Response({"valid": True}, status=status.HTTP_200_OK)
        except (TokenError, InvalidToken):
            return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response({'data':'Successfully logout'}, status=status.HTTP_200_OK)
    




class ProfileView(APIView):
    permission_classes = [IsAuthenticated]   # only logged-in users
    
    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff
        })

    def put(self, request):
        user = request.user
        user.email = request.data.get("email", user.email)
        user.save()
        return Response({"message": "Profile updated successfully"})

