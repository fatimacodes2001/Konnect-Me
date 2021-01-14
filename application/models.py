# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Album(models.Model):
    objects = models.Manager()
    album_id = models.AutoField(primary_key=True)
    page_email = models.ForeignKey('Page', models.DO_NOTHING, db_column='page_email', blank=True, null=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email', blank=True, null=True)
    album_col = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    num_photos = models.IntegerField(blank=True, null=True)

    class Meta:
                 db_table = 'album'


class AppliesFor(models.Model):
    objects = models.Manager()
    job = models.OneToOneField('Job', models.DO_NOTHING, primary_key=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email')

    class Meta:
        db_table = 'applies_for'
        unique_together = (('job', 'regular_profile_email'),)


class Interests(models.Model):
    objects = models.Manager()
    email = models.OneToOneField('RegularProfile', models.DO_NOTHING, db_column='email', primary_key=True)
    interest = models.CharField(max_length=45)

    class Meta:
        db_table = 'interests'
        unique_together = (('email', 'interest'),)


class Job(models.Model):
    objects = models.Manager()
    job_id = models.AutoField(primary_key=True)
    page_email = models.ForeignKey('Page', models.DO_NOTHING, db_column='page_email')
    type = models.CharField(max_length=50, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    num_posts = models.IntegerField(blank=True, null=True)
    num_hours = models.IntegerField(blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    contact_detail = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    postdate = models.DateTimeField(blank=True, null=True)

    class Meta:
                 db_table = 'job'
                 get_latest_by = 'job_id'



class Page(models.Model):
    objects = models.Manager()
    email = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=45, blank=True, null=True)
    businessid = models.IntegerField(db_column='businessId', blank=True, null=True)  # Field name made lowercase.
    companytype = models.CharField(db_column='companyType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=45, blank=True, null=True)
    aboutyou = models.CharField(db_column='aboutYou', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    numfollowers = models.IntegerField(db_column='numFollowers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
                 db_table = 'page'


class PageFollowsPage(models.Model):
    objects = models.Manager()
    follower_email = models.OneToOneField(Page, models.DO_NOTHING, db_column='follower_email', primary_key=True)
    followed_page_email = models.ForeignKey(Page, models.DO_NOTHING, db_column='followed_page_email',related_name='+')

    class Meta:
        db_table = 'page_follows_page'
        unique_together = (('follower_email', 'followed_page_email'),)


class PageFollowsProfile(models.Model):
    objects = models.Manager()
    follower_page_email = models.OneToOneField(Page, models.DO_NOTHING, db_column='follower_page_email', primary_key=True)
    followed_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='followed_profile_email')

    class Meta:
        db_table = 'page_follows_profile'
        unique_together = (('follower_page_email', 'followed_profile_email'),)


class PageLikesPhotos(models.Model):
    objects = models.Manager()
    update = models.OneToOneField('Photos', models.DO_NOTHING, primary_key=True)
    page_email = models.ForeignKey(Page, models.DO_NOTHING, db_column='page_email')
    photo_like_id = models.IntegerField()

    class Meta:
        db_table = 'page_likes_photos'
        unique_together = (('update', 'page_email', 'photo_like_id'),)


class PageLikesStatus(models.Model):
    objects = models.Manager()
    update = models.OneToOneField('Status', models.DO_NOTHING, primary_key=True)
    page_email = models.ForeignKey(Page, models.DO_NOTHING, db_column='page_email')
    status_like_id = models.IntegerField()

    class Meta:
        db_table = 'page_likes_status'
        unique_together = (('update', 'page_email', 'status_like_id'),)


class Photos(models.Model):
    objects = models.Manager()
    update_id = models.AutoField(primary_key=True)
    status_id = models.IntegerField()
    album = models.ForeignKey(Album, models.DO_NOTHING)
    page_email = models.ForeignKey(Page, models.DO_NOTHING, db_column='page_email', blank=True, null=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email', blank=True, null=True)
    caption = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    num_likes = models.IntegerField(blank=True, null=True)
    num_lhares = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
                 db_table = 'photos'
                 get_latest_by = 'update_id'



class ProfileFollowsPage(models.Model):
    objects = models.Manager()
    page_email = models.OneToOneField(Page, models.DO_NOTHING, db_column='page_email', primary_key=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email')

    class Meta:
        db_table = 'profile_follows_page'
        unique_together = (('page_email', 'regular_profile_email'),)


class ProfileFollowsProfile(models.Model):
    objects = models.Manager()
    follower_email = models.OneToOneField('RegularProfile', models.DO_NOTHING, db_column='follower_email', primary_key=True)
    followed_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='followed_profile_email',related_name='+')

    class Meta:
        db_table = 'profile_follows_profile'
        unique_together = (('follower_email', 'followed_profile_email'),)


class ProfileLikesPhotos(models.Model):
    objects = models.Manager()
    update = models.OneToOneField(Photos, models.DO_NOTHING, primary_key=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email')
    photo_like_id = models.IntegerField()

    class Meta:
        db_table = 'profile_likes_photos'
        unique_together = (('update', 'regular_profile_email', 'photo_like_id'),)


class ProfileLikesStatus(models.Model):
    objects = models.Manager()
    update = models.OneToOneField('Status', models.DO_NOTHING, primary_key=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email')
    status_like_id = models.IntegerField()

    class Meta:
        db_table = 'profile_likes_status'
        unique_together = (('update', 'regular_profile_email', 'status_like_id'),)


class ProfileSharesPhotos(models.Model):
    objects = models.Manager()
    update = models.OneToOneField(Photos, models.DO_NOTHING, primary_key=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email')
    share_id = models.IntegerField()

    class Meta:
        db_table = 'profile_shares_photos'
        unique_together = (('update', 'regular_profile_email', 'share_id'),)


class ProfileSharesStatus(models.Model):
    objects = models.Manager()
    update = models.OneToOneField('Status', models.DO_NOTHING, primary_key=True)
    regular_profile_email = models.ForeignKey('RegularProfile', models.DO_NOTHING, db_column='regular_profile_email')
    share_id = models.IntegerField()

    class Meta:
                 db_table = 'profile_shares_status'
                 unique_together = (('update', 'regular_profile_email', 'share_id'),)


class RegularProfile(models.Model):
    objects = models.Manager()
    email = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=45, blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    about_you = models.CharField(max_length=1000, blank=True, null=True)
    work_profile = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    p_grad = models.CharField(max_length=250, blank=True, null=True)
    u_grad = models.CharField(max_length=250, blank=True, null=True)
    high_school = models.CharField(max_length=250, blank=True, null=True)
    further_education = models.CharField(db_column='Further_education', max_length=250, blank=True, null=True)  # Field name made lowercase.
    num_followers = models.IntegerField(blank=True, null=True)

    class Meta:
                 db_table = 'regular_profile'


class Skills(models.Model):
    objects = models.Manager()
    email = models.OneToOneField(RegularProfile, models.DO_NOTHING, db_column='email', primary_key=True)
    skill = models.CharField(max_length=45)

    class Meta:
        db_table = 'skills'
        unique_together = (('email', 'skill'),)


class Status(models.Model):
    objects = models.Manager()
    update_id = models.AutoField(primary_key=True)
    status_id = models.IntegerField()
    regular_profile_email = models.ForeignKey(RegularProfile, models.DO_NOTHING, db_column='regular_profile_email', blank=True, null=True)
    page_email = models.ForeignKey(Page, models.DO_NOTHING, db_column='page_email', blank=True, null=True)
    caption = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    num_shares = models.IntegerField(blank=True, null=True)
    num_likes = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
                 db_table = 'status'
                 get_latest_by = 'update_id'
