import os
import random
import string
import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


def random_id(n=8, no_upper=False, no_lower=False, no_digit=False):
    rand = random.SystemRandom()
    chars = ''
    if no_upper is False:
        chars += string.ascii_uppercase
    if no_lower is False:
        chars += string.ascii_lowercase
    if no_digit is False:
        chars += string.digits
    if not chars:
        raise Exception('chars is empty! change function args!')
    return ''.join([rand.choice(chars) for _ in range(n)])


def get_random_upload_path(upload_dir, filename, include_date=False):
    ext = filename.split('.')[-1]
    randid = random_id(n=8)
    filename = "{0}-{1}.{2}".format(uuid.uuid4(), randid, ext)
    if include_date:
        filename = '{}-{}'.format(timezone.now().strftime('%Y%m%d%H%M%S'), filename)
    return os.path.join(upload_dir, filename)


def avatar_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'user', 'avatar'), filename)


def sponsor_log_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'sponsor', 'logo'), filename)


def photo_original_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'photo', 'original'), filename)


def photo_low_resolution_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'photo', 'low_resolution'), filename)


def photo_thumbnail_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'photo', 'thumbnail'), filename)


class User(AbstractUser):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'
    GENDER_UNKNOWN = 'u'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
        (GENDER_UNKNOWN, 'Unknown'),
    )
    email = models.EmailField(null=True, unique=True)
    is_photographer = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=avatar_file_path_func)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if self.username:
            self.username = self.username.lower()
        super().save(*args, **kwargs)


class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='photographer')
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    street_address = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sponsor')
    brand_name = models.CharField(max_length=256, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True, upload_to=sponsor_log_file_path_func)
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    street_address = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Tag(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tag')

    def __str__(self):
        return str(self.name)


class Photo(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='photo')
    tags = models.ManyToManyField(Tag)
    original = models.ImageField(upload_to=photo_original_file_path_func)
    low_resolution = models.ImageField(upload_to=photo_low_resolution_file_path_func, editable=False)
    thumbnail = models.ImageField(upload_to=photo_thumbnail_file_path_func, editable=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    archive_datetime = models.BooleanField(null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    @property
    def archived(self):
        return self.archive_datetime is not None

    def __str__(self):
        return str(self.title)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='cart')
    create_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.photo)


class PhotoOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_order')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_order')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    create_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.photo)
