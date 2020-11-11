from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated

from api.validation import check_email
from api.models import Course, UserProfile
from api.serializers import UserSerializer, UserProfileSerializer, ResetPasswordEmailRequestSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, generics

from settings import logger

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def create(self, request):
        if all(value != None for value in request.data.values()):
            email = request.data.get("email")
            username = request.data.get("username")
            password = request.data.get("password") or request.data.get("password1")
            logger.info(f"TRYING SERIALIZE NEW USER: {request.data}")

            serializer = UserSerializer(data={"username":username, "email":email, "password":password}) 
            if serializer.is_valid():
                serializer.save()
                logger.info(f"NEW USER CREATED: {serializer.data} ")
                new_user = User.objects.get(email=email, username=username)
                if UserProfile.objects.create(user=new_user, id = new_user.id, user_courses = []):
                    logger.info(f"USER PROFILE WAS CREATED - {new_user.id}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"NEW USER WAS NOT CREATED {serializer.data} BECAUSE OF {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            logger.error(f"NEW USER WAS NOT CREATED - SOME EMPTY INPUT FIELDS: {request.data}")
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        

class UserProfileClass(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-id')
    serializer_class = UserProfileSerializer


@api_view(['POST'])
def search_userprofile(request):
    if request.data:
        req = request.data.dict()
        if req.get("password"):
            if req.get("username") or req.get("email"):
                if check_email(req.get("username")):
                    req["email"] = req["username"]
                    del req["username"]
                if User.objects.filter(**req).exists():
                    user = User.objects.get(**req)
                    user_profile = UserProfile.objects.get(user=user)
                    data = {**UserSerializer(user).data, **UserProfileSerializer(user_profile).data}
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    logger.error(f"User {req} was not found")
                    return Response(f"User {req} was not found", status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error(f"Unauthorized, request without password: {req} ")
            return Response(f"Unauthorized, request without password, req: {req} ", status=status.HTTP_401_UNAUTHORIZED)

    logger.error("Request with empty body")
    return Response("Request with empty body", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def search_user_by_email(request):
    email = request.data.get("email")

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        data = {**UserSerializer(user).data}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# def change_password(request):
#     user = User.objects.all()
#     serializer = ChangePasswordSerializer(data=request.data)
#
#     if serializer.is_valid():
#         # Check old password
#         if not user.check_password(serializer.data.get("old_password")):
#             return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#         # set_password also hashes the password that the user will get
#         user.set_password(serializer.data.get("new_password"))
#         user.save()
#         response = {
#             'status': 'success',
#             'code': status.HTTP_200_OK,
#             'message': 'Password updated successfully',
#             'data': []
#         }
#
#         return Response(response)
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)