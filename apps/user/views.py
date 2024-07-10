from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .utils import send_verification_email
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer 


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class VerifyEmail(APIView):
    def get(self, request, verification_token):
        user = get_object_or_404(User, verification_token=verification_token)
        if user.is_verified:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save(update_fields= ["is_verified"]) 
        return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        print("**************************************")
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            print("User--------------------------------->", user)
            token, created = Token.objects.get_or_create(user=user)
            print("################################")
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK) 


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

