import os

from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import LazyObject
from phonenumber_field.modelfields import PhoneNumberField
from six import BytesIO


def avatar_file_path_func(instance, filename):
    from lastweekend_photos.helpers.utils import get_random_upload_path
    return get_random_upload_path(os.path.join('uploads', 'user', 'avatar'), filename)


def sponsor_log_file_path_func(instance, filename):
    from lastweekend_photos.helpers.utils import get_random_upload_path
    return get_random_upload_path(os.path.join('uploads', 'sponsor', 'logo'), filename)


def photo_original_file_path_func(instance, filename):
    from lastweekend_photos.helpers.utils import get_random_upload_path
    return get_random_upload_path(os.path.join('uploads', 'photo', 'original'), filename)


def photo_low_res_file_path_func(instance, filename):
    from lastweekend_photos.helpers.utils import get_random_upload_path
    return get_random_upload_path(os.path.join('uploads', 'photo', 'low_res'), filename)


def photo_preview_file_path_func(instance, filename):
    from lastweekend_photos.helpers.utils import get_random_upload_path
    return get_random_upload_path(os.path.join('uploads', 'photo', 'preview'), filename)


def photo_ads_file_path_func(instance, filename):
    from lastweekend_photos.helpers.utils import get_random_upload_path
    dirpath = ('uploads', 'photo_ads')
    if instance.id:
        return os.path.join(*dirpath, os.path.split(filename)[-1])
    return get_random_upload_path(os.path.join(*dirpath), filename)


class PublicStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PUBLIC_FILE_STORAGE)()


public_storage = PublicStorage()


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
    sponsors = models.ManyToManyField(Sponsor, blank=True)

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
    preview_file = models.ImageField(upload_to=photo_preview_file_path_func, editable=False,
                                     storage=public_storage)
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
        from lastweekend_photos.helpers.utils import resize_photo
        if not self.pk:
            resize_photo(self.original_file, self.low_res_file, scale=settings.PHOTO_LOW_RES_SCALE)
            resize_photo(self.low_res_file, self.preview_file, scale=settings.PHOTO_PREVIEW_RES_SCALE)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class PhotoAds(models.Model):

    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_ads')
    ads_sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, related_name='photo_ads')
    ads_position = models.CharField(max_length=2, choices=Photo.LOGO_POSITION_CHOICES)
    file = models.ImageField(upload_to=photo_ads_file_path_func, editable=False, storage=public_storage)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('photo', 'ads_sponsor', 'ads_position'),)

    def make_file_with_ads(self):
        from lastweekend_photos.helpers.utils import paste_logos

        file_name = self.file.name
        low_res_file = self.photo.low_res_file
        if not file_name:
            file_name = low_res_file.name

        # file_name = file_name.lstrip(self.file.field.upload_to)
        _, file_ext = os.path.splitext(file_name)
        if file_ext in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif file_ext == '.gif':
            FTYPE = 'GIF'
        elif file_ext == '.png':
            FTYPE = 'PNG'
        else:
            raise Exception('Not supported format "{}"'.format(file_ext))

        image = Image.open(low_res_file)
        sponsors = [s for s in self.photo.event.sponsors.order_by('id').all() if s != self.ads_sponsor]
        if self.ads_sponsor:
            sponsors.append(self.ads_sponsor)
        logos = [s.logo for s in sponsors if s.logo]
        if logos:
            paste_logos(image, logos, position=self.ads_position, logo_width=settings.PHOTO_LOGO_WIDTH,
                        x_margin=settings.PHOTO_LOGO_X_MARGIN, y_margin=settings.PHOTO_LOGO_Y_MARGIN)

        temp_file = BytesIO()
        image.save(temp_file, FTYPE)
        temp_file.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.file.save(file_name, ContentFile(temp_file.read()), save=False)
        temp_file.close()

    def save(self, *args, **kwargs):
        generate_file = kwargs.pop('_generate_file', True)
        if generate_file:
            self.make_file_with_ads()
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.photo)


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
