from django.db import models

from core.models import Portals


class SettingsPortal(models.Model):
    """Модель настроек портала"""

    portal = models.OneToOneField(
        Portals,
        verbose_name='Портал',
        related_name='settings_portal',
        on_delete=models.CASCADE,
    )
    quantity_pallet_code = models.CharField(
        'Код поля количество паллет',
        help_text='Код поля количество паллет в сделке',
        default='UF_CRM_0000000000',
        max_length=30,
    )
    tonnage_code = models.CharField(
        'Код поля тоннаж',
        help_text='Код поля тоннаж в сделке',
        default='UF_CRM_0000000000',
        max_length=30,
    )

    class Meta:
        verbose_name = 'Настройка портала'
        verbose_name_plural = 'Настройки портала'

        ordering = ['portal', 'pk']

    def __str__(self):
        return 'Настройки для портала {}'.format(self.portal.name)
