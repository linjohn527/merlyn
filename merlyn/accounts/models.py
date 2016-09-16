# _*_ coding:utf-8 _*_

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
import django


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
            Creates and saves a User with the given email, date of
                birth and password.
            """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        :param email:
        :param name:
        :param password:
        :return:
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    token = models.CharField(u'token', max_length=255, default=None, blank=True, null=True)
    department = models.CharField(u'部门', max_length=32, default=None, blank=True, null=True)
    telephone = models.CharField(u'固定电话', max_length=32, default=None, blank=True, null=True)
    mobile = models.CharField(u'手机', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField(u'备注', default=None, blank=True, null=True)
    date_join = models.DateTimeField(u'创建时间', auto_now_add=True, blank=True)
    valid_time = models.DateTimeField(u'生效时间', default=django.utils.timezone.now)
    invalid_time = models.DateTimeField(u'失效时间', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def get_full_name(self):
        """
        The user is identified by their email address
        :return:
        """
        return self.email

    def get_short_name(self):
        """
        The user is identified by their email address
        :return:
        """
        return self.email

    def __str__(self):
        """

        :return:
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        :param perm:
        :param obj:
        :return:
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`
        :param app_label:
        :return:
        """
        return True


    def is_staff(self):
        """
        Is the user a member of staff?
        :return:
        """
        return self.is_admin

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'