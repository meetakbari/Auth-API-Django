from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.authentication import get_authorization_header

from .serializers import UserSerializer
from .models import User
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token

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

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True) 
        #httponly true means only on backend one can access that cookie, on frontend side it is not accesible.
    
        response.data = {
            'token': access_token
        }

        return response

class UserAPIView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = User.objects.filter(pk=id).first()
            print(UserSerializer(user).data)
            return Response(UserSerializer(user).data)
        
        raise AuthenticationFailed('unauthenticated')   

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    def post(self, _): # _ means that parameter will not be used
        response = Response()
        response.delete_cookie(key='refreshToken')
        response.data = {
            'message': 'logged out successfully!'
        }

        return response