from rest_framework import serializers
from datetime import date
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('iin', 'name', 'surname', 'birth_date', 'phone', 'avatar', 'user_type', 'password', 're_password')
        extra_fields = {'password': {'write_only': True}}

    def validate(self, attrs):
        if len(attrs['iin'])!=12:
            raise serializers.ValidationError({'iin': 'IIN must match'})

        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({'password': 'Password must match'})

        if(attrs['birth_date'] < date(1900, 1, 1)):
            raise serializers.ValidationError({'birth_date': 'not match'})
            
        return attrs

    def save(self):
        del self.validated_data['re_password']
        account = User(**self.validated_data)
        password = self.validated_data['password']
        account.set_password(password)
        account.save()

class BaseUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'user_type', 'last_login')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'iin', 'name', 'surname', 'full_name', 'phone', 'avatar', 'birth_date', 'user_type', 'is_superuser', 'last_login')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'iin', 'name', 'surname', 'full_name', 'phone', 'avatar', 'birth_date', 'user_type')
        read_only_fields = ('id', 'iin', 'full_name')
