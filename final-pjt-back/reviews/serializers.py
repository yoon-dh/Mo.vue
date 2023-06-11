from rest_framework import serializers
from .models import Review,Comment

class ReviewListSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comment_set = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    like_reviews = serializers.PrimaryKeyRelatedField(many = True,read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializers(serializers.ModelSerializer):
    # movie = serializers.CharField(read_only=True)
    # user = serializers.CharField(read_only=True)
    # review_like = serializers.CharField(read_only=True)
    # board_num = serializers.CharField(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user','like_users',)


class CommentSerailizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review','user',)
