
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """ Managers for user"""

    def create_user(self, username, email, password=None, **extra_field):
        """ create, save and return new user. """
        if not email:
            raise ValueError('Email is required for signup process')

        user = self.model(
            username=username,
            email=self.normalize_email(
                email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password=None):
        """ create, save and return super user. """
        user = self.create_user(
            username=username, email=email, password=password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    is_room_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    profile_picture = models.ImageField(
        upload_to='core/pofile_pictures', default="avatar.svg", null=True)
    city = models.CharField(max_length=200, null=True)
    bio = models.TextField(max_length=250, null=True)


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)

    class Meta:
        ordering = ['-modified_at', 'created_at']

    def __str__(self):
        return self.name


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'created_at']

    def __str__(self):
        return self.message[0:50]
