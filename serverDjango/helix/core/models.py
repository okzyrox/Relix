from django.db import models

from datetime import timedelta

# Create your models here.

class Certification(models.Model):
    certName = models.CharField(max_length=100, null=False, blank=False)
    certId = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return (f"{self.certId} - {self.certName}")

class banType(models.Model):
    typeName = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.typeName}"

class banInstance(models.Model):
    robloxId = models.CharField(max_length=50, null=False, blank=False)
    banReason = models.TextField(max_length=130, blank=True, null=True)
    banType = models.ForeignKey(banType, null=True, on_delete=models.SET_NULL)
    banStart = models.DateTimeField(auto_now_add=True)
    banLength = models.DurationField()

    def __str__(self):
        return f"Ban for id: {self.robloxId}, started:{self.banStart}, length:{self.banLength}"

class robloxUser(models.Model):
    robloxId = models.CharField(max_length=50, null=False, blank=False, unique=True)
    is_banned = models.BooleanField(null=False, blank=False, default=False)
    banData = models.ForeignKey(banInstance, null=True, blank=True, on_delete=models.CASCADE)
    has_drivers_license = models.BooleanField(null=False, blank=False, default=False)
    suspended_license = models.BooleanField(null=False, blank=False, default=False)
    
    active = models.BooleanField(null=False, blank=False, default=False)

    userCerts = models.ManyToManyField(Certification)

    def __str__(self):
        return f"Account for: {self.robloxId}"