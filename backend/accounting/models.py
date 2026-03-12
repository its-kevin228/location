from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('late', 'En retard'),
        ('partial', 'Partiel'),
    ]
    METHOD_CHOICES = [
        ('cash', 'Espèces'),
        ('bank_transfer', 'Virement bancaire'),
        ('check', 'Chèque'),
        ('mobile_money', 'Mobile Money'),
    ]

    lease = models.ForeignKey(
        'tenants.Lease', on_delete=models.PROTECT, related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Montant (FCFA)'
    )
    due_date = models.DateField(verbose_name="Date d'échéance")
    paid_date = models.DateField(null=True, blank=True, verbose_name='Date de paiement')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Statut'
    )
    method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, blank=True, verbose_name='Méthode de paiement'
    )
    reference = models.CharField(
        max_length=100, blank=True, verbose_name='Référence'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-due_date']

    def __str__(self):
        return f'Paiement {self.amount} FCFA — {self.lease} ({self.get_status_display()})'


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('works', 'Travaux'),
        ('tax', 'Taxe / Impôt'),
        ('agency_fee', "Frais d'agence"),
        ('co_ownership', 'Copropriété'),
        ('other', 'Autre'),
    ]

    property = models.ForeignKey(
        'properties.Property', on_delete=models.CASCADE, related_name='expenses'
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name='Catégorie'
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Montant (FCFA)'
    )
    date = models.DateField(verbose_name='Date')
    description = models.TextField(blank=True, verbose_name='Description')
    invoice = models.FileField(
        upload_to='accounting/invoices/', blank=True, null=True, verbose_name='Facture'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dépense'
        verbose_name_plural = 'Dépenses'
        ordering = ['-date']

    def __str__(self):
        return f'{self.get_category_display()} — {self.amount} FCFA ({self.date})'


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='audit_logs'
    )
    action = models.CharField(max_length=50, verbose_name='Action')  # create, update, delete
    model_name = models.CharField(max_length=100, verbose_name='Modèle')
    object_id = models.CharField(max_length=50, verbose_name='ID objet')
    old_value = models.JSONField(null=True, blank=True, verbose_name='Ancienne valeur')
    new_value = models.JSONField(null=True, blank=True, verbose_name='Nouvelle valeur')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Horodatage')

    class Meta:
        verbose_name = 'Journal d\'audit'
        verbose_name_plural = 'Journal d\'audit'
        ordering = ['-timestamp']

    def __str__(self):
        return f'[{self.timestamp:%Y-%m-%d %H:%M}] {self.action} {self.model_name} #{self.object_id}'
