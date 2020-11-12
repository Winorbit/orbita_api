from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import UserProfile
from api.serializers import UserSerializer, UserProfileSerializer
from api.validation import check_email
from settings import EMAIL_HOST_USER
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

            serializer = UserSerializer(data={"username": username, "email": email, "password": password})
            if serializer.is_valid():
                serializer.save()
                logger.info(f"NEW USER CREATED: {serializer.data} ")
                new_user = User.objects.get(email=email, username=username)
                if UserProfile.objects.create(user=new_user, id=new_user.id, user_courses=[]):
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

    req = request.data
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


def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@api_view(['POST'])
def send_email_for_orbita(request):
    user_message = request.data.get('message')
    user_email = request.data.get('email')
    if user_message and not user_message.isspace() and validate_email(user_email):
        body = f"\nFrom to: {user_email}\nMessage: {user_message}"
        try:
            send_mail('Feedback', body, EMAIL_HOST_USER, ['winorbita@gmail.com'], fail_silently=False)
        except Exception as e:
            logger.error(f"USER MESSAGE WAS NOT SENT - {e}")
            return Response({"ERROR": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)
    else:
        logger.error(f"USER FEEDBACK HAVE NOT VALID DATA - 'email': {user_email}, 'message': {user_message}")
        return Response({"email": user_email, "message": user_message}, status=status.HTTP_400_BAD_REQUEST)
