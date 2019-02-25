from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.pagination import PageNumberPagination
import json
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle  # 限速
from rest_framework.decorators import detail_route, list_route

from .serializer import (LikeSerializer, FollowSerializer, CollectSerializer, DownloadSerializer, CommentLikeSerialzer,
                         LikeListSerializer, DownloadListSerializer, FollowListSerializer, FanListSerializer,
                         ApplicationListSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer,
                         ReportSerializer)
from .models import LikeShip, Follow, UserFolderImage, DownloadShip, CommentLike, Application
from users.models import EmailVerifyRecord, UserMessage
from images.models import ImageModel
from utils.send_email import send_xx_email

User = get_user_model()


class ReportViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        举报评论
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = ReportSerializer


class FollowUserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全部关注用户
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = FollowListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Follow.objects.filter(fan=self.request.user)


class FanUserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全部粉丝
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = FanListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(follow=self.request.user)


class CollectViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加图片到收藏夹
    destroy:
        从收藏夹删除图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = CollectSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 删除只能是该用户收藏
        return UserFolderImage.objects.filter(user=self.request.user)


class LikeViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户点赞图片
    create:
        点赞一张图片
    destroy:
        取消点赞一张图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = LikeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return LikeListSerializer
        return LikeSerializer

    def get_queryset(self):
        # 删除只能是点赞者
        return LikeShip.objects.filter(user=self.request.user)


class FollowViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        关注用户
    destroy:
        取消关注
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = FollowSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return FollowSerializer

    def get_queryset(self):
        # 取消只能是关注者
        return Follow.objects.filter(fan=self.request.user)


class DownloadPagination(PageNumberPagination):
    """
    图片分页
    page_size: 每页大小
    page_size_query_param: 每页大小参数名
    page_query_param: 第几页参数名
    max_page_size: 最大页数
    """
    page_size = 8
    page_size_query_param = 'num'
    page_query_param = "page"
    max_page_size = 100


class DownloadViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    create:
        下载图片
    list:
        获取用户下载图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = DownloadSerializer
    pagination_class = DownloadPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return DownloadShip.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DownloadListSerializer
        return DownloadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ship = self.perform_create(serializer)
        re_dict = serializer.data
        re_dict['url'] = 'http://' + self.request._request.META['HTTP_HOST'] + ship.image.image.url

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class CommentLikeViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加点赞评论
    destroy:
        取消点赞评论
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = CommentLikeSerialzer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return CommentLike.objects.filter(user=self.request.user)


class ApplicationViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取个人签约状态
    create:
        添加签约申请
    update:
        修改申请状态
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = ApplicationListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            serializer.data[0]['status'] = int(serializer.data[0]['status'])
            return Response(serializer.data[0])
        return Response({'status': 0})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.status != 1:
            return Response({'error': '没有同意合约'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        serializer.data['status'] = int(serializer.data['status'])
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ship = self.perform_create(serializer)
        ship.status = '1'
        ship.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        elif self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationUpdateSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


