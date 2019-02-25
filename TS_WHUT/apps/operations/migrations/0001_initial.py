# Generated by Django 2.0.7 on 2018-11-24 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', '用户同意合同'), ('2', '等待审核'), ('4', '未通过审核'), ('3', '已完成')], default='2', max_length=11, verbose_name='申请签约状态')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '申请签约',
                'verbose_name_plural': '申请签约',
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '点赞评论',
                'verbose_name_plural': '点赞评论',
            },
        ),
        migrations.CreateModel(
            name='DownloadShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='下载时间')),
            ],
            options={
                'verbose_name': '下载图片',
                'verbose_name_plural': '下载图片',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='关注时间')),
            ],
            options={
                'verbose_name': '关注用户',
                'verbose_name_plural': '关注用户',
            },
        ),
        migrations.CreateModel(
            name='LikeShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='点赞时间')),
            ],
            options={
                'verbose_name': '点赞图片',
                'verbose_name_plural': '点赞图片',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='评论内容')),
                ('reason', models.CharField(max_length=150, verbose_name='举报理由')),
                ('status', models.CharField(choices=[('1', '等待审核'), ('2', '举报通过'), ('3', '举报不通过')], default='1', max_length=11, verbose_name='审核状态')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='举报时间')),
            ],
            options={
                'verbose_name': '举报评论',
                'verbose_name_plural': '举报评论',
            },
        ),
        migrations.CreateModel(
            name='UserFolderImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '收藏图片',
                'verbose_name_plural': '收藏图片',
            },
        ),
    ]
