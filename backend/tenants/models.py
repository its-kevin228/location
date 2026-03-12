from django.db import models
from django.conf import settings


class Tenant(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tenant_profile',
        limit_choices_to={'role': 'tenant'}
    )
    first_name = models.CharField(max_length=100, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, verbose_name='Nom')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Téléphone')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date de naissance')
    profession = models.CharField(max_length=150, blank=True, verbose_name='Profession')
    id_document = models.FileField(
        upload_to='tenants/id_documents/', blank=True, null=True,
        verbose_name="Pièce d'identité"
    )
    # Garant
    guarantor_name = models.CharField(max_length=200, blank=True, verbose_name='Nom du garant')
    guarantor_phone = models.CharField(max_length=20, blank=True, verbose_name='Téléphone du garant')
    guarantor_document = models.FileField(
        upload_to='tenants/guarantors/', blank=True, null=True,
        verbose_name='Document garant'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Locataire'
        verbose_name_plural = 'Locataires'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Lease(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('active', 'Actif'),
        ('terminated', 'Résilié'),
    ]

    property = models.ForeignKey(
        'properties.Property', on_delete=models.PROTECT, related_name='leases'
    )
    tenant = models.ForeignKey(
        Tenant, on_delete=models.PROTECT, related_name='leases'
    )
    start_date = models.DateField(verbose_name="Date d'entrée")
    end_date = models.DateField(null=True, blank=True, verbose_name='Date de sortie')
    rent_amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Loyer HC (FCFA)'
    )
    charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Charges (FCFA)'
    )
    deposit_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Dépôt de garantie (FCFA)'
    )
    annual_revision_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        verbose_name='Taux de révision annuelle (%)'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Statut'
    )
    signed_contract = models.FileField(
        upload_to='leases/contracts/', blank=True, null=True,
        verbose_name='Contrat signé'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bail'
        verbose_name_plural = 'Baux'
        ordering = ['-start_date']

    def __str__(self):
        return f'Bail {self.tenant} — {self.property} ({self.start_date})'
