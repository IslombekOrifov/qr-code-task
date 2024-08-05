from django.db import models


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.user_id} -> {self.full_name}"


class Pricing(models.Model):
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.price_per_hour}"


class UserQrCode(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='qr_codes', on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/')
    uid = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_end = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.user_id} -> {self.id}"