from django.contrib.auth import login, logout, authenticate

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import json

from instagram.models import User, Post, Comment, Like, FollowRelation
from instagram import serializers


class NewsfeedListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.PostSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            posts = Post.objects.filter(user=user)
            all_following = FollowRelation.objects.filter(follower__username=user.username).values('user')
            for item in all_following:
                pk = item['user']
                user = User.objects.get(pk=pk)
                posts = posts | Post.objects.filter(user__username=user.username)
            serializer = serializers.PostSerializer(posts, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            serializer = serializers.UserLoginSerializer(request.data)
            user = authenticate(**serializer.data)
            token = Token.objects.get_or_create(user=user)
            print(token[0])
            user_credentials = {
                'username': serializer.data["username"],
                'token': token[0]
                }
            login(request, user)

            return Response(json.dumps(user_credentials))
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserSignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.initial_data['username']
        first_name = serializer.initial_data['first_name']
        last_name = serializer.initial_data['last_name']
        email = serializer.initial_data['email']
        password = serializer.initial_data['password']
        date_of_birth = serializer.initial_data['date_of_birth']
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            password=password,
        )
        return Response(serializer.data)


class UsernameEmailAvailableAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        filters = {}
        if "username" in request.data:
            filters["username"] = request.data["username"]
        elif "email" in request.data:
            filters["email"] = request.data["email"]
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        is_taken = User.objects.filter(**filters).exists()
        return Response({"is_taken": is_taken})


class UserListAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    lookup_field = 'pk'


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostDetailSerializer


class LikeListAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer


class LikeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
