from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


def clean_existing_user_values(query_param, instance, validation_class):
    message = _("{value} is already used by another user.")
    error = {
        key: message.format(field=key.capitalize(), value=val)
        for key, val in query_param.items()
    }

    def _error_or_delete():
        if user.is_active:
            raise validation_class(error)
        elif user.pk:
            user.delete()

    try:
        user = User.objects.get(**query_param)
        for key, val in query_param.items():
            field = user._meta.get_field(key).verbose_name
            error = {key: message.format(field=field.capitalize(), value=val)}
    except User.DoesNotExist:
        pass
    except User.MultipleObjectsReturned:
        qs = User.objects.filter(**query_param)

        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)

        if qs.filter(is_active=True).exists():
            raise validation_class(error)
        else:
            qs.filter(is_active=False).delete()
    else:
        if instance:
            if instance.pk != user.pk:
                _error_or_delete()
            return  # no need to delete if it is the same instance
        else:
            _error_or_delete()


class Country(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class User(AbstractUser):
    MALE = "male"
    FEMALE = "female"
    GENDER = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )
    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER, default=MALE, max_length=8)
    age = models.IntegerField(null=True)
    country = models.ForeignKey(
        Country, related_name="country_users", on_delete=models.CASCADE, null=True
    )
    city = models.ForeignKey(
        City, related_name="city_users", on_delete=models.CASCADE, null=True
    )

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username
