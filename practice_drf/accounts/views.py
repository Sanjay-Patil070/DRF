from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..practice_api.models import *
from ..practice_api.serializer import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout


# Create your views here.
class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        # Validate required fields
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #  Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #  Create user with hashed password
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # important: hashes password
        )

        return Response(
            {"message": "User created successfully", "user_id": user.id},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate required fields
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, user.password):
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username,
                "access_token": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,  # set to True in production (HTTPS)
            samesite="Lax",  # or 'None' if cross-domain
            max_age=86400,  # 1 day
        )
        return response


class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token missing"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            response = Response({"access": new_access})
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),  # rotates
                httponly=True,
                secure=True,
                samesite="None",
            )
            return response
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=401)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token missing"}, status=400)

            refresh = RefreshToken(refresh_token)
            refresh.blacklist()  # Blacklist the refresh token

            response = Response({"message": "Logout successful"}, status=200)
            response.delete_cookie("refresh_token")
            return response
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=401)
