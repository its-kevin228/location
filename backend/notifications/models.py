from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('unpaid', 'Loyer impayé'),
        ('lease_end', 'Fin de bail proche'),
        ('revision', 'Révision de loyer'),
        ('document_ready', 'Document disponible'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name='Type'
    )
    title = models.CharField(max_length=200, verbose_name='Titre')
    message = models.TextField(verbose_name='Message')
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.title} → {self.user}'


class Document(models.Model):
    TYPE_CHOICES = [
        ('receipt', 'Quittance de loyer'),
        ('lease', 'Contrat de bail'),
        ('certificate', 'Attestation'),
    ]

    lease = models.ForeignKey(
        'tenants.Lease', on_delete=models.CASCADE, related_name='documents'
    )
    payment = models.ForeignKey(
        'accounting.Payment', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='documents'
    )
    type = models.CharField(
        max_length=15, choices=TYPE_CHOICES, verbose_name='Type de document'
    )
    file = models.FileField(
        upload_to='documents/', blank=True, null=True, verbose_name='Fichier'
    )
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Généré le')
    sent_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Envoyé le'
    )

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-generated_at']

    def __str__(self):
        return f'{self.get_type_display()} — {self.lease}'
