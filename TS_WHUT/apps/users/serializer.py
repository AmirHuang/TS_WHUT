# _*_ coding: utf-8 _*_
# @time     : 2018/11/24
# @Author   : Amir
# @Site     : 
# @File     : serializer.py
# @Software : PyCharm

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from .models import Folder, Org
from operations.models import UserFolderImage, Follow
from images.models import ImageModel

User = get_user_model()


class OrgOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ('id', 'status')


class OrgSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Org
        fields = ('image', 'teacher', 'name', 'id', 'user')


class FolderOneSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField()

    def get_results(self, obj):
        data = []
        ships = UserFolderImage.objects.filter(folder_id=obj.id)
        for ship in ships:
            image = ship.image
            data.append({
                "ship_id": ship.id,
                'image': 'http://' + self.context['request']._request.META['HTTP_HOST'] + image.image['avatar'].url,
                "add_time": image.add_time,
                "desc": image.desc,
                "user": image.user.id,
                "pattern": image.pattern,
                "like_nums": image.like_nums,
                "cates": image.cates,
                "collection_nums": image.collection_nums,
                "download_nums": image.download_nums,
                "name": image.name,
                "id": image.id,
            })
        return data

    class Meta:
        model = Folder
        fields = ('name', 'id', 'nums', 'results', 'desc', 'add_time', 'update_time')


class FolderListSerializer(serializers.ModelSerializer):
    if_collect = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        data = []
        base_url = 'http://' + self.context['request']._request.META['HTTP_HOST']
        print('-------------')
        print('base_url:', base_url)
        ships = UserFolderImage.objects.filter(folder_id=obj.id)
        for i, ship in enumerate(ships):
            if i == 4:
                return data
            print(ship.image.image)
            print(ship.image.image['avatar'])
            print(ship.image.image['avatar'].url)
            data.append({
                'url': base_url + ship.image.image['avatar'].url
            })
        return data

    def get_if_collect(self, obj):
        image_id = self.context['request'].query_params.get('image-id')
        if image_id:
            ship = UserFolderImage.objects.filter(image_id=image_id,
                                                  user=self.context['request'].user,
                                                  folder=obj)
            if ship.count():
                return ship[0].id
        return False

    class Meta:
        model = Folder
        fields = ('name', 'id', 'nums', 'if_collect', 'image', 'desc', 'add_time', 'update_time')


class FolderCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if Folder.objects.filter(user=self.context['request'].user).count() > 50:
            raise serializers.ValidationError('收藏夹数量已达上限')
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Folder
        fields = ('name', 'id', 'desc')


class FolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'id', 'desc')


class UserListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    if_follow = serializers.SerializerMethodField()

    def get_if_follow(self, obj):
        ship = Follow.objects.filter(fan_id=self.context['request'].user.id,
                                     follow_id=obj.id)
        if ship:
            return ship[0].id
        return False

    def get_images(self, obj):
        data = []
        i = 0
        for image in ImageModel.objects.filter(user=obj, if_active=True)[::-1]:
            i += 1
            if i > 3:
                return data
            data.append({
                'url': 'http://' + self.context['request']._request.META['HTTP_HOST'] + image.image['avatar'].url,
                'id': image.id
            })
        return data

    class Meta:
        model = User
        fields = (
            'id', 'if_sign', 'follow_nums', 'fan_nums', 'upload_nums', 'like_nums', 'desc', 'qq', 'email', 'p_class',
            'if_cer', 'org_name', 'collection_nums', 'download_nums', 'image', 'username', 'images', 'if_follow')


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名', required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='密码',
                                     max_length=16, min_length=6, required=True,
                                     error_messages={'max_length': '密码长度应该在6到12个字符之间',
                                                     'min_length': '密码长度应该在6到12个字符之间'})

    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='再次输入密码',
                                             required=True)

    def validate(self, attrs):
        username = attrs['username']
        users = User.objects.filter(username=username)
        if users.count():
            user = users[0]
            if user.is_active:
                raise serializers.ValidationError('用户名已经存在')
            else:
                user.delete()

        email = attrs['email']
        users = User.objects.filter(email=email)
        if users.count():
            user = users[0]
            if user.is_active:
                raise serializers.ValidationError('邮箱已经存在')
            else:
                user.delete()

        password = attrs['password']
        password_confirm = attrs['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError('密码不一致')

        del attrs['password_confirm']
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password_confirm', 'username')


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='用户名', help_text='用户名', required=False, allow_blank=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='用户名已经存在')])
    email = serializers.CharField(label='邮箱', required=False, allow_blank=True,
                                  validators=[UniqueValidator(queryset=User.objects.all(),
                                                              message='邮箱已经存在')])
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='密码',
                                     max_length=16, min_length=6, required=False,
                                     error_messages={'max_length': '密码长度应该在6到12个字符之间',
                                                     'min_length': '密码长度应该在6到12个字符之间'})

    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='再次输入密码',
                                             required=False)

    def validate(self, attrs):
        if attrs.get('password') and attrs.get('password_confirm'):
            if attrs['password'] == attrs['password_confirm']:
                attrs['password'] = make_password(attrs['password'])
            else:
                raise serializers.ValidationError('密码不一致')

        if attrs.get('email'):
            user = self.context['request'].user.if_active
            user.is_active = False
            user.save()

        del attrs['password_confirm']
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password_confirm',
                  'desc', 'username', 'image', 'gender', 'birthday', 'qq', 'p_class')


class SmsSerializer(serializers.Serializer):
    email = serializers.EmailField()
