"""TS_WHUT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin

from django.views.static import serve
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from TS_WHUT.settings import MEDIA_ROOT
from users.views import OrgViewset, FolderViewset
from images.views import GroupsViewset, ImageViewset, SmallGroupsViewset
from images.views import CommentViewset, BannerViewset
from operations.views import ReportViewset, FollowUserViewset, FanUserViewset, CollectViewset
from operations.views import LikeViewset, FollowViewset
from users.views import UserViewset
router = DefaultRouter()

# router.register('reset', ResetEmailViewset, base_name='reset')

# 认证API
router.register('certification', OrgViewset, base_name="certification")

# 收藏夹API
router.register('folders', FolderViewset, base_name="folders")

# 大类别API
router.register('big_group', GroupsViewset, base_name="big_group")

# 图片API
router.register('images', ImageViewset, base_name="images")

# 小类别API
router.register('group', SmallGroupsViewset, base_name="group")

# 评论API
router.register('comment', CommentViewset, base_name="comment")

# 举报评论
router.register('report', ReportViewset, base_name="report")

# 关注者API
router.register('followers', FollowUserViewset, base_name="followings")

# 粉丝API
router.register('fans', FanUserViewset, base_name="fans")

# 收藏API
router.register('collect', CollectViewset, base_name="collect")

# 点赞API
router.register('like', LikeViewset, base_name="like")

# 关注API
router.register('follow', FollowViewset, base_name="follow")

# 用户API
router.register('users', UserViewset, base_name="users")

# 轮播图API
router.register('banners', BannerViewset, base_name="banners")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),

    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),

    # drf 文档，title自定义
    path('docs', include_docs_urls(title='Amir')),

    path('api-auth/', include('rest_framework.urls')),

    re_path('^', include(router.urls)),
]
