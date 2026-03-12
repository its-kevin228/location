from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrateur'),
        ('owner', 'Propriétaire/Agence'),
        ('tenant', 'Locataire'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='owner')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'
