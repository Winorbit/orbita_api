from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import UserSerializer, UserProfileSerializer
from api.models import UserProfile, Group
from api.validation import check_email
from settings import logger


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def create(self, request):
        if all(value != None for value in request.data.values()):
            email = request.data.get("email")
            username = request.data.get("username")
            password = request.data.get("password") or request.data.get("password1")

            if not request.data.get("is_staff"):
                is_staff = False
            else:
                is_staff = True

            if not request.data.get("is_superuser"):
                is_superuser = False
            else:
                is_superuser = True

            logger.info(f"Trying serialize new user: {request.data}")

            if User.objects.filter(email=email): 
                logger.info(f"User with email {email} already exist")
                return Response(status=status.HTTP_409_CONFLICT)
 
            if User.objects.filter(username=username):
                logger.info(f"User with username {username} already exist")
                return Response(status=status.HTTP_409_CONFLICT)
            
            new_user_info = {"username": username, 
                             "email": email, 
                             "password": password, 
                             "is_superuser": is_superuser, 
                             "is_staff": is_staff}

            serializer = UserSerializer(data=new_user_info)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"New user created: {serializer.data} ")
                new_user = User.objects.get(email=email, username=username)
                new_user.set_password(password)
                new_user.save()
                if UserProfile.objects.create(user=new_user, id=new_user.id):
                    logger.info(f"User profile were created - {new_user.id}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"New user were not created {serializer.data} because of {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            logger.error(f"New user were not created - some empty fields: {request.data}")
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)


class UserProfileClass(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-id')
    serializer_class = UserProfileSerializer


@api_view(['POST'])
def search_userprofile(request):
    req = request.data
    if req.get("password"):
        if req.get("username") or req.get("email"):
            if req.get("email") and not req.get("username"):
                user_email=req.get("email")
                if not check_email(user_email):
                    logger.error(f"Not valid user email: {user_email}")
                    return Response(f"User email is incorrect: {req}", status=status.HTTP_404_NOT_FOUND)

            """use email like username 
            """
            password = req["password"]
            if req.get("username"):
                if check_email(req.get("username")):
                    req["email"]=req.get("username")
                    del req["username"]

            # unhashed password broke pipelin
            del req["password"]
            
            if User.objects.filter(**req).exists():
                user = User.objects.get(**req)
                if not user.check_password(password):
                    return Response(f"Unauthorized, request without password, req: {req} ", status=status.HTTP_401_UNAUTHORIZED)
                user_profile = UserProfile.objects.get(user=user)
                data = {**UserSerializer(user).data, **UserProfileSerializer(user_profile).data}
                return Response(data, status=status.HTTP_200_OK)
            else:
                logger.error(f"Not valid user data: {req}")
                return Response(f"User {req} was not found", status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error(f"Request with invalid body: {req}")
            return Response(f"Request with empty body: {req}", status=status.HTTP_400_BAD_REQUEST)
    else:
        logger.error(f"Unauthorized, request without password: {req} ")
        return Response(f"Unauthorized, request without password, req: {req} ", status=status.HTTP_401_UNAUTHORIZED)


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
    new_user_info = dict(request.data.dict())
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

@api_view(["PUT"])
def add_user_to_group(request):
    data = request.data
    if not data:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user_id  = data.get("user_id")
    group_id  = data.get("group_id")

    if user_id and group_id:
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            Group.objects.get(id=group_id)
        except Exception as e:
            logger.info(f"Failed with exception: {e}")
            return Response({"message": f"Failed with exception: {e}"}, status=status.HTTP_404_NOT_FOUND)

        if group_id in user_profile.groups:
            logger.info(f"User {user_profile} already member of group {group_id}")
            return Response({"message": f"User is already in this group"}, status=status.HTTP_409_CONFLICT)
        else:
            user_profile.groups.append(group_id)
            user_profile.save()
            logger.info(f"Group {group_id} was added user {user_profile}")
            return Response(status=status.HTTP_200_OK)
    else:
        logger.info(f"User with id {user_id} was not found")
        return Response({"message": f"User with id {user_id} was not found"}, status=status.HTTP_404_NOT_FOUND)
