# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    type = models.ForeignKey('Type', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('ArticleUserinfor', models.DO_NOTHING, blank=True, null=True)
    supportcount = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'article'


class ArticleUserinfor(models.Model):
    username = models.CharField(max_length=11)
    password = models.CharField(max_length=11)
    email = models.CharField(max_length=22, blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    imgurl = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    score = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'article_userinfor'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comment(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING, blank=True, null=True)
    comment_content = models.TextField()
    user = models.ForeignKey(ArticleUserinfor, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comment'


class Danmu(models.Model):
    vid = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    dsize = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    dtime = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'danmu'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Follow(models.Model):
    follower = models.IntegerField(blank=True, null=True)
    followee = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follow'


class Manager(models.Model):
    username = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'manager'


class Message(models.Model):
    content = models.TextField(blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'message'


class Sample(models.Model):
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed =True
        db_table = 'sample'


class Support(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    article_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'support'


class Type(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed =True
        db_table = 'type'


class Usermessage(models.Model):
    content = models.CharField(max_length=255, blank=True, null=True)
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    time = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed =True
        db_table = 'usermessage'


class Vcomment(models.Model):
    userid = models.IntegerField(blank=True, null=True)
    vid = models.IntegerField(blank=True, null=True)
    ctime = models.CharField(max_length=255, blank=True, null=True)
    mycomment = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vcomment'


class Video(models.Model):
    video_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'video'


class Videolist(models.Model):
    vname = models.CharField(max_length=255)
    vurl = models.CharField(max_length=255)
    descp = models.CharField(max_length=255, blank=True, null=True)
    seenum = models.BigIntegerField()
    zhan = models.BigIntegerField(blank=True, null=True)
    imgurl = models.CharField(max_length=255)
    vsource = models.CharField(max_length=255)
    publictime = models.CharField(max_length=255, blank=True, null=True)
    videotp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'videolist'


class Videotype(models.Model):
    id = models.IntegerField(primary_key=True)
    typename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'videotype'
