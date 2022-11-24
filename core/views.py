from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from .serializers import UserSerializer
from .models import User

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()

        if not user:
            raise APIException('Invalid credentials')
        
        if not user.check_password(request.data['password']):
            raise APIException('Invalid credentials')

        serializer = UserSerializer(user)

        return Response(serializer.data)
    
