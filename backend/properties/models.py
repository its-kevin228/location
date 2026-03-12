from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nom')
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Nom icône (ex: home, building)')

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='property_types'
    )

    class Meta:
        verbose_name = 'Type de bien'
        verbose_name_plural = 'Types de biens'
        ordering = ['category', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Équipement')

    class Meta:
        verbose_name = 'Équipement'
        verbose_name_plural = 'Équipements'
        ordering = ['name']

    def __str__(self):
        return self.name


class Property(models.Model):
    LISTING_TYPES = [
        ('rent', 'Location'),
        ('sale', 'Vente'),
        ('both', 'Location & Vente'),
    ]
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('rented', 'Loué'),
        ('sold', 'Vendu'),
        ('under_construction', 'En travaux'),
        ('reserved', 'Réservé'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='properties', limit_choices_to={'role': 'owner'}
    )
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='properties'
    )
    equipments = models.ManyToManyField(Equipment, blank=True, related_name='properties')

    title = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, verbose_name='Adresse')
    city = models.CharField(max_length=100, verbose_name='Ville')
    surface = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Surface (m²)'
    )
    rooms = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Pièces')

    listing_type = models.CharField(
        max_length=10, choices=LISTING_TYPES, default='rent', verbose_name='Type d\'annonce'
    )
    rent_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Loyer HC (FCFA)'
    )
    charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Charges (FCFA)'
    )
    sale_price = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Prix de vente (FCFA)'
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='Statut'
    )
    lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='Latitude'
    )
    lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='Longitude'
    )
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bien immobilier'
        verbose_name_plural = 'Biens immobiliers'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} — {self.city}'


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='photos'
    )
    image = models.ImageField(upload_to='properties/')
    is_main = models.BooleanField(default=False, verbose_name='Photo principale')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f'Photo {self.pk} — {self.property.title}'


class Sale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En cours'),
        ('signed', 'Signé'),
        ('cancelled', 'Annulé'),
    ]

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='sales'
    )
    buyer_name = models.CharField(max_length=200, verbose_name="Nom de l'acheteur")
    buyer_email = models.EmailField(blank=True)
    buyer_phone = models.CharField(max_length=20, blank=True)
    sale_price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name='Prix de vente (FCFA)'
    )
    sale_date = models.DateField(null=True, blank=True, verbose_name='Date de vente')
    notary_fees = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Frais de notaire (FCFA)'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Statut'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['-created_at']

    def __str__(self):
        return f'Vente {self.property.title} → {self.buyer_name}'
