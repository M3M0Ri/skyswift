import shortuuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
# from PIL import Image
from shortuuid.django_fields import ShortUUIDField

Gender = (
    ("male", "Male"),
    ("femail", "Femail")
)

level = (
    ("agency", "Agency"),
    ("normal", "Normal")
)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, ext),
    return f"user_{instance.user.id}/{filename}"


class MyUserModel(AbstractUser):
    full_name = models.CharField(max_length=200, default="")
    username = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True, default="")
    phone = models.CharField(max_length=200, default="")
    gender = models.CharField(max_length=100, choices=Gender)
    role = models.CharField(max_length=10, default="normal")
    otp = models.CharField(max_length=10, null=True, blank=True, default="")
    charge = models.PositiveIntegerField(default=0 , validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=22,
                         alphabet='abcdefghijklmnopqrstuvwxyz')

    user = models.OneToOneField(MyUserModel, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to=user_directory_path,
                                    default="cover.jpg", blank=True)
    image = models.ImageField(upload_to=user_directory_path,
                              default="default.jpg", blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=Gender, default="male")
    about_me = models.TextField(max_length=200, null=True)

    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    working_at = models.CharField(max_length=200, null=True, blank=True)

    instagram = models.CharField(max_length=200, null=True, blank=True)

    verified = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        # if self.full_name != "" or self.full_name is not None:
        # return self.full_name
        # else:
        return self.user.username

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.full_name) + "-" + str(uniqueid.lower())
        super(Profile, self).save(*args, **kwargs)

def creat_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(creat_user_profile, sender=MyUserModel)
post_save.connect(save_user_profile, sender=MyUserModel)
