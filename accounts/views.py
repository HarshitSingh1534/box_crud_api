# Create your views here.
from accounts.serializers import LoginUserSerializer, RegisterStaffSerializer
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import status
from rest_framework.response import Response


class SignupStaffUserView(APIView):
    """
    Signup a staff user.
    """

    serializer_class = RegisterStaffSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "success": "True",
            "message": "Staff user created successfully",
        }

        return Response(response, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    """
    Login a user.
    """

    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            "success": "True",
            "message": "User logged in successfully",
            "token": serializer.validated_data["token"].key,
        }

        return Response(response, status=status.HTTP_200_OK)


class LogoutUserView(APIView):
    """
    Logout a user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        response = {
            "success": "True",
            "message": "User logged out successfully",
        }

        return Response(response, status=status.HTTP_200_OK)
