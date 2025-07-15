from EcommerceInventory.permission import IsSuperAdmin
from EcommerceInventory.Helpers import renderResponse
from UserServices.models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate

class SignupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        profile_pic = request.data.get('profile_pic')

        if not all([username, email, password]):
            return renderResponse(
                data=None,
                message='Please provide username, email, and password',
                status=status.HTTP_400_BAD_REQUEST
            )

        if Users.objects.filter(email=email).exists():
            return renderResponse(
                data=None,
                message='Email already exists',
                status=status.HTTP_400_BAD_REQUEST
            )

        if Users.objects.filter(username=username).exists():
            return renderResponse(
                data=None,
                message='Username already exists',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = Users.objects.create_user(
            username=username,
            email=email,
            password=password,
            profile_pic=profile_pic
        )

        domain_user_id = request.data.get('domain_user_id')
        if domain_user_id:
            try:
                user.domain_user_id = Users.objects.get(id=domain_user_id)
            except Users.DoesNotExist:
                return renderResponse(
                    data=None,
                    message='Invalid domain_user_id',
                    status=status.HTTP_400_BAD_REQUEST
                )

        user.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access['username'] = user.username
        access['email'] = user.email
        access['profile_pic'] = user.profile_pic.url if user.profile_pic else ""

        return renderResponse(
            data={
                'access': str(access),
                'refresh': str(refresh),
            },
            message='User created successfully',
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not all([username, password]):
            return renderResponse(
                data=None,
                message='Please provide both username and password',
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access['username'] = user.username
            access['email'] = user.email
            access['profile_pic'] = user.profile_pic.url if user.profile_pic else ""

            return renderResponse(
                data={
                    'access': str(access),
                    'refresh': str(refresh),
                },
                message='Login successful',
                status=status.HTTP_200_OK
            )

        return renderResponse(
            data=None,
            message='Invalid credentials',
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        return renderResponse(
            data=None,
            message='Please use POST method to login',
            status=status.HTTP_400_BAD_REQUEST
        )


class PublicAPIView(APIView):
    def get(self, request):
        return renderResponse(
            data='This is a publicly accessible API',
            message='This is a publicly accessible API',
            status=status.HTTP_200_OK
        )


class ProtectedAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return renderResponse(
            data='This is a protected API.',
            message='Authenticated access granted',
            status=status.HTTP_200_OK
        )


class SuperAdminCheckApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        return renderResponse(
            data='This is a Super Admin API.',
            message='Super Admin access granted',
            status=status.HTTP_200_OK
        )
