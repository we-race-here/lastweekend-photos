import os
import random
import string
import uuid

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from six import BytesIO


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


def photo_low_res_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'photo', 'low_res'), filename)


def photo_preview_file_path_func(instance, filename):
    return get_random_upload_path(os.path.join('uploads', 'photo', 'preview'), filename)


def resize_photo(origin_field, resized_field, scale=100):
    new_name, new_extension = os.path.splitext(origin_field.name)
    new_extension = new_extension.lower()

    new_filename = new_name + '_size{}'.format(scale) + new_extension

    if new_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif new_extension == '.gif':
        FTYPE = 'GIF'
    elif new_extension == '.png':
        FTYPE = 'PNG'
    else:
        raise Exception('Not supported format "{}"'.format(new_extension))

    image = Image.open(origin_field).copy()
    new_size = (scale, scale)
    x, y = image.size

    if x > scale and y > scale:
        if x > y:
            ratio = max(y / scale, 1)
            new_size = (int(max(x / ratio, 1)), scale)
        elif x < y:
            ratio = max(x / scale, 1)
            new_size = (scale, int(max(y / ratio, 1)))
        image.thumbnail(new_size, Image.ANTIALIAS)

    # Save resizednail to in-memory file as StringIO
    temp_resized = BytesIO()
    image.save(temp_resized, FTYPE)
    temp_resized.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    resized_field.save(new_filename, ContentFile(temp_resized.read()), save=False)
    temp_resized.close()

    return True


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


class Event(models.Model):
    name = models.CharField(max_length=128, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=128)
    map_latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True)
    map_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)


class PhotoTag(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='photo_tag')

    class Meta:
        unique_together = (('name', 'user',),)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class PhotoPeople(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='photo_people')

    class Meta:
        unique_together = (('name', 'user',),)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Photo(models.Model):
    LOGO_POSITION_TL = 'tl'
    LOGO_POSITION_TC = 'tc'
    LOGO_POSITION_TR = 'tr'
    LOGO_POSITION_CL = 'cl'
    LOGO_POSITION_CC = 'cc'
    LOGO_POSITION_CR = 'cr'
    LOGO_POSITION_BL = 'bl'
    LOGO_POSITION_BC = 'bc'
    LOGO_POSITION_BR = 'br'
    LOGO_POSITION_CHOICES = (
        (LOGO_POSITION_TL, 'Top-Left'),
        (LOGO_POSITION_TC, 'Top-Center'),
        (LOGO_POSITION_TR, 'Top-Right'),
        (LOGO_POSITION_CL, 'Center-Left'),
        (LOGO_POSITION_CC, 'Center-Center'),
        (LOGO_POSITION_CR, 'Center-Right'),
        (LOGO_POSITION_BL, 'Bottom-Left'),
        (LOGO_POSITION_BC, 'Bottom-Center'),
        (LOGO_POSITION_BR, 'Bottom-Right'),
    )
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='photo')
    tags = models.ManyToManyField(PhotoTag, blank=True)
    peoples = models.ManyToManyField(PhotoPeople, blank=True)
    original_file = models.ImageField(upload_to=photo_original_file_path_func)
    low_res_file = models.ImageField(upload_to=photo_low_res_file_path_func, editable=False)
    preview_file = models.ImageField(upload_to=photo_preview_file_path_func, editable=False)
    logo_position = models.CharField(max_length=2, choices=LOGO_POSITION_CHOICES, default=LOGO_POSITION_BR)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    downloads = models.PositiveIntegerField(default=0)
    seen = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, related_name='photo')
    photo_date = models.DateField(null=True, blank=True)
    archive_datetime = models.DateTimeField(null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    @property
    def archived(self):
        return self.archive_datetime is not None

    def save(self, *args, **kwargs):
        if not self.pk:
            resize_photo(self.original_file, self.low_res_file, scale=settings.PHOTO_LOW_RES_SCALE)
            resize_photo(self.low_res_file, self.preview_file, scale=settings.PHOTO_PREVIEW_RES_SCALE)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='cart')
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'photo',),)

    def __str__(self):
        return str(self.photo)


class PhotoOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_order')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_order')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'photo',),)

    def __str__(self):
        return str(self.photo)
