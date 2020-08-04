from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, User, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, required=False)

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,
                                        slug_field='username',
                                        default=CurrentUserDefault())
    following = serializers.SlugRelatedField(read_only=False,
                                             slug_field='username',
                                             queryset=User.objects.all())

    def validate(self, data):
        following = data['following']
        if following == self.context['request'].user:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя')
        return data

    class Meta:
        model = Follow
        fields = ['user', 'following']
        validators = [UniqueTogetherValidator
                      (queryset=Follow.objects.all(),
                       fields=['user', 'following'])]
