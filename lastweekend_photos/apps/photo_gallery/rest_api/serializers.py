from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.core import exceptions as django_exceptions

from apps.photo_gallery.models import User, Photographer, Sponsor
from lastweekend_photos.helpers.utils import DynamicFieldsSerializerMixin, Base64ImageField


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'})
    remember = serializers.BooleanField(initial=False, required=False)


class PermissionSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'})
    current_password = serializers.CharField(style={'input_type': 'password'})

    default_error_messages = {
        'invalid_password': 'Invalid Password',
    }

    def validate_current_password(self, value):
        is_password_valid = self.context['request'].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail('invalid_password')

    def validate_new_password(self, new_password):
        try:
            validate_password(new_password, self.context['request'].user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return new_password


class NestedGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class UserSessionSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    user_permissions = PermissionSerializer(read_only=True, many=True)
    groups = NestedGroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ('password',)


class PhotographerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'
        read_only_fields = ('user',)


class SponsorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'
        read_only_fields = ('user',)


class UserProfileSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    photographer = PhotographerProfileSerializer(required=False, allow_null=True)
    sponsor = SponsorProfileSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'avatar', 'is_photographer',
                  'photographer', 'is_sponsor', 'sponsor')
        read_only_fields = ('email', 'username')

    @transaction.atomic()
    def update(self, instance, validated_data):
        photographer_data = validated_data.pop('photographer', {})
        if photographer_data:
            try:
                photographer_object = instance.photographer
            except Photographer.DoesNotExist:
                photographer_object = None
            if not photographer_object:
                photographer_object = Photographer(user=instance)
            for k, v in photographer_data.items():
                setattr(photographer_object, k, v)
            photographer_object.save()

        sponsor_data = validated_data.pop('sponsor', {})
        if sponsor_data:
            try:
                sponsor_object = instance.sponsor
            except Sponsor.DoesNotExist:
                sponsor_object = None
            if not sponsor_object:
                sponsor_object = Sponsor(user=instance)
            for k, v in sponsor_data.items():
                setattr(sponsor_object, k, v)
            sponsor_object.save()

        return super(UserProfileSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        res = super(UserProfileSerializer, self).to_representation(instance)
        if not res.get('photographer'):
            res['photographer'] = {}
        if not res.get('sponsor'):
            res['sponsor'] = {}
        return res
