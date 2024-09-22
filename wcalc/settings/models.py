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
    # package_name = models.CharField(
    #     'Название упаковки',
    #     help_text='Текстовое поле, размер 1024 символа',
    #     max_length=1024,
    #     default=''
    # )
    # weight = models.FloatField(
    #     'Создавать элемент смарт процесса',
    #     help_text='Число с плавающей точкой, два знака после запятой',
    #
    # )

    class Meta:
        verbose_name = 'Настройка портала'
        verbose_name_plural = 'Настройки портала'

        ordering = ['portal', 'pk']

    def __str__(self):
        return 'Настройки для портала {}'.format(self.portal.name)
