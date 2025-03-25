from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from account.serializers import LoginSerializer, SignupSerializer
from account.models import BlacklistToken
class ProtectedView(viewsets.GenericViewSet):

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def viewDashboard(self, request):
        return Response({"message": "This is a protected view! for dashboard api's"})

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def viewprofile(self, request):
        return Response({"message": "This is a protected view for profile"})


class AuthAPIView(viewsets.GenericViewSet):

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {"refresh": str(refresh), "access": access_token},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                try:
                    BlacklistToken.objects.create(token=refresh_token)
                    return Response(
                        {"message": "Successfully logged out."},
                        status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    return Response(
                        {"error": f"An error occurred: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred during logout: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )