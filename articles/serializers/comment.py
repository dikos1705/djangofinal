from rest_framework import serializers
from articles.models.comment import Comment
from user.serializers import BaseUserInfoSerializer


class CommentSerializer(serializers.ModelSerializer):
    owner = BaseUserInfoSerializer(read_only=True)

    def to_representation(self, instance):
        self.fields['replies'] = CommentSerializer(many=True, read_only=True, context={"request": self.context['request']})
        return super(CommentSerializer, self).to_representation(instance)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'reply', 'replies', 'owner')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'reply')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        validated_data['article_id'] = self.context['view'].kwargs['id']
        return super().create(validated_data)
