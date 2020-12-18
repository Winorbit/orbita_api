from os import environ
from django.contrib.auth.models import User
from django.core.mail import send_mail

from api.validation import check_email
from api.models import Course, UserProfile
from api.serializers import UserSerializer, UserProfileSerializer

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import UserProfile
from api.serializers import UserSerializer, UserProfileSerializer
from api.validation import check_email
from settings import EMAIL_HOST_USER, logger, RESTORE_ACCESS_MESSAGE_TEMPLATE

from Crypto.Cipher import XOR
import base64
from datetime import datetime

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
 

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


def check_if_user_exist_by_field(field, value):
    if User.objects.filter(**{field:value}).exists():
        return True
    else:
        return False

@api_view(["PUT"])
def update_user_info(request, user_id):
    new_user_info = dict(request.data)
    if not new_user_info:
        logger.info(f"Empty request body for update user {user_id}")
        return Response({"message": "Empty request body"}, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=user_id)
    if not user:
        logger.info(f"User {user} was not found")
        return Response({"message": f"User with id {user_id} was not found"}, status=status.HTTP_404_NOT_FOUND)

    if user and new_user_info:
        for key, value in new_user_info.copy().items():
            if not new_user_info.get(key):
                del new_user_info[key]

        for (key, value) in new_user_info.items():
            if check_if_user_exist_by_field(key, value): 
                logger.info(f"User with {key}: {value} already exist")
                return Response({"message": f"User with {key}: {value} already exist"}, status=status.HTTP_409_CONFLICT)
        for (key, value) in new_user_info.items():
            setattr(user, key, value)
        user.save()

        logger.info(f"User {user} was updated with values {new_user_info}")
        return Response(status=status.HTTP_202_ACCEPTED)

def validate_user_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@api_view(['POST'])
def send_email_for_orbita(request):
    user_message = request.data.get('message')
    user_email = request.data.get('email')
    if user_message and not user_message.isspace() and validate_user_email(user_email):
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


def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext)).decode("utf-8")


def create_restore_access_url(root_url:str, email: str, datetime:str, cypher_key:str)->str:
    hashed_datetime = encrypt(cypher_key,datetime).decode("utf-8")
    hashed_email = encrypt(cypher_key,email).decode("utf-8")
    restore_access_url = f"{root_url}/{hashed_email}||{hashed_datetime}"
    return restore_access_url
    pass


@api_view(['POST'])
def send_restore_access_email(request):
    user_email = request.data.get('email')
    if user_email:
        try:
            user = User.objects.get(email=user_email)
        except Exception as e:

            return Response({"message": f"Error with search user {e}"}, status=status.HTTP_404_NOT_FOUND)

        root_url = f"{environ.get('UI_HOST')}/restore/"
        date_time_now = datetime.now().strftime("%Y.%m.%d.%H")
        cypher_key = environ.get("CYPHER_KEY")
        restore_link = create_restore_access_url(root_url, user_email, date_time_now, cypher_key)

        restore_access_message = f"{RESTORE_ACCESS_MESSAGE_TEMPLATE}\n{restore_link}"
        try:
            res = send_mail("Востановление доступа к профилю 'Зимней Орбиты'", restore_access_message, EMAIL_HOST_USER, [user_email], fail_silently=False)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Email was not correctly sended because of {e}"},status=status.HTTP_406_NOT_ACCEPTABLE)
    else: 
        return Response({"message": "Email in request not presnts"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_user_password(request):
    hashed_string = request.data.get("hashed_user_info")
    new_password = request.data.get("password")
    if hashed_string and new_password:
        if "||" in hashed_string:
            logger.info(f"trying to decoded {hashed_string}")
            cypher_key = environ.get("CYPHER_KEY")
            encoded_email = hashed_string.split("||")[0]
            encoded_datetime = hashed_string.split("||")[1]
        else: 
            return Response({"message": f"hashed string  {hashed_string} is invalid "}, status=status.HTTP_400_BAD_REQUEST)

        decoded_email = decrypt(cypher_key,encoded_email)
        decoded_datetime = decrypt(cypher_key, encoded_datetime)

        logger.info(f"Decoded data from request - {encoded_email}, {encoded_datetime}")
        
        logger.info(f"Trying to validate decoded email - {decoded_email}")
        if not validate_user_email(decoded_email):
            return Response({"message": f"email from hased string is invalid - {decoded_email}, please, check string and cypher key"}, status=status.HTTP_400_BAD_REQUEST)
        
        now = datetime.now()
        decoded_datetime_to_list  = [int(x) for x in decoded_datetime.split(".")]
        link_generation_time = datetime(*decoded_datetime_to_list)
        duration = now - link_generation_time
        duration_in_hours = divmod(duration.total_seconds(), 3600)[0]
        logger.info(f"trying to check by datetime duration if link still available.  Now - {now}, time from link - {link_generation_time}")

        if duration_in_hours > 24:
            return Response({f"message": "Link expired, older then 24 hours - (duration in hours)"},status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            try:
                logger.info(f"Trying to extract user by email {decoded_email}")
                user = User.objects.get(email=decoded_email)
            except Exception as e:
                logger.error(f"Can't find user by email {decoded_email}")
                return Response({"message": f"Error with search user {e}"}, status=status.HTTP_404_NOT_FOUND)
        logger.info(f"Trying to change user password from {user.password} to {new_password}") 
        if user.password == new_password: 
            logger.error(f"Unseccessfull attempt to update password - new password equal with old - old:{user.password} new:{new_password}")
            return Response({"message": f"Sorry, this user already use this password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.password=new_password
            user.save()
            logger.info(f"Password for user was updated")
            return Response({"message": f"Password for user was updated on {user.password}"},status=status.HTTP_200_OK)
        
    else: 
        logger.info(f"Request does not conatain hashed_string or new password. Request body: {request.data}")
        return Response({"message": "Not hashed_user_info in request"},status=status.HTTP_404_NOT_FOUND)
