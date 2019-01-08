from rest_framework import serializers

from instagram.models import User, FollowRelation, Post, Like, Comment


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post', 'timestamp')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'text', 'timestamp')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user', 'image', 'text',)


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'image', 'text', 'created_at', 'like_set', 'comment_set',)


class FollowRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = ('id', 'followee', 'follower')


class UserDetailSerializer(serializers.ModelSerializer):
    followee = serializers.PrimaryKeyRelatedField(many=True, queryset=FollowRelation.objects.all())
    follower = serializers.PrimaryKeyRelatedField(many=True, queryset=FollowRelation.objects.all())

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'date_of_birth',
                  'avatar',
                  'bio',
                  'followee',
                  'follower',
                  'post_set'
                  )


class UserSerializer(serializers.ModelSerializer):
    followee = serializers.PrimaryKeyRelatedField(many=True, queryset=FollowRelation.objects.all())
    follower = serializers.PrimaryKeyRelatedField(many=True, queryset=FollowRelation.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'followee', 'follower')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password',
                  'date_of_birth',
                  ]


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  ]
