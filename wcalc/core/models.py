from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания и дату обновления"""

    created = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated = models.DateField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    class Meta:
        abstract = True


class Portals(models.Model):
    """Модель портала Битрикс24"""
    member_id = models.CharField(
        verbose_name='Уникальный код портала',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя портала',
        max_length=255,
    )
    auth_id = models.CharField(
        verbose_name='Токен аутентификации',
        max_length=255,
    )
    auth_id_create_date = models.DateTimeField(
        verbose_name='Дата получения токена аутентификации',
        auto_now=True,
    )
    refresh_id = models.CharField(
        verbose_name='Токен обновления',
        max_length=255,
    )
    client_id = models.CharField(
        verbose_name='Уникальный ID клиента',
        max_length=50,
        null=True,
        blank=True,
    )
    client_secret = models.CharField(
        verbose_name='Секретный токен клиента',
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Портал'
        verbose_name_plural = 'Порталы'

    def __str__(self):
        return self.name


class ProductRow(CreatedModel):
    """Модель Товарной позиции."""

    PRODUCTROW_ID = models.PositiveIntegerField('ID товарной позиции', db_index=True, )
    OWNER_ID = models.PositiveIntegerField('ID владельца')
    OWNER_TYPE = models.CharField('Тип владельца', max_length=256)
    PRODUCT_ID = models.PositiveIntegerField('ID товара в каталоге')
    PRODUCT_NAME = models.CharField('Наименование товарной позиции', max_length=1024)
    ORIGINAL_PRODUCT_NAME = models.CharField('Наименование товара в каталоге', max_length=1024)
    PRODUCT_DESCRIPTION = models.TextField('Описание товара', null=True, blank=True)
    PRICE = models.DecimalField(
        'Цена со скидкой и налогом',
        help_text='Цена за единицу товарной позиции с учетом скидок и налогов',
        max_digits=12, decimal_places=2, null=True
    )
    PRICE_EXCLUSIVE = models.DecimalField(
        'Цена со скидкой, без налога',
        help_text='Цена за единицу товарной позиции с учетом скидок, но без учета налогов',
        max_digits=12, decimal_places=2, null=True
    )
    PRICE_NETTO = models.DecimalField(
        'Цена без скидки, без налога',
        help_text='Цена за единицу товарной позиции без учета скидок и без учета налогов',
        max_digits=12, decimal_places=2, null=True
    )
    PRICE_BRUTTO = models.DecimalField(
        'Цена с налогом, без скидки',
        help_text='Цена за единицу товарной позиции с учетом налогов, но без учета скидок',
        max_digits=12, decimal_places=2, null=True
    )
    PRICE_ACCOUNT = models.DecimalField(
        'Цена со скидкой и налогом в валюте отчетов',
        help_text='Цена за единицу товарной позиции с учетом скидок и налогов, конвертированная в валюту отчетов',
        max_digits=12, decimal_places=2, null=True
    )
    QUANTITY = models.DecimalField('Количество', max_digits=12, decimal_places=2, null=True)
    DISCOUNT_TYPE_ID = models.PositiveSmallIntegerField(
        'Тип скидки',
        help_text='Может быть 1 для скидки в абсолютном значении и 2 для скидки в процентах. По умолчанию равно 2'
    )
    DISCOUNT_RATE = models.DecimalField('Процент скидки', max_digits=5, decimal_places=2, null=True)
    DISCOUNT_SUM = models.DecimalField('Сумма скидки', max_digits=12, decimal_places=2, null=True)
    TAX_RATE = models.DecimalField('Процент налога', max_digits=5, decimal_places=2, null=True, blank=True)
    TAX_INCLUDED = models.CharField(
        'Налог включен в цену',
        help_text='Может иметь значения "Y" или "N"',
        max_length=2
    )
    CUSTOMIZED = models.CharField(
        'Кастомизированное',
        help_text='Может иметь значения "Y" или "N". Назначение поля неизвестно',
        max_length=2
    )
    MEASURE_CODE = models.PositiveIntegerField('Код единицы измерения')
    MEASURE_NAME = models.CharField('Единица измерения', max_length=10)
    SORT = models.PositiveIntegerField('Сортировка')
    XML_ID = models.CharField('XML_ID', null=True, blank=True, max_length=256)
    TYPE = models.PositiveSmallIntegerField(
        'Тип товарной позиции',
        help_text='1 - простой товар, 4 - торговое предложение/вариация'
    )
    STORE_ID = models.PositiveSmallIntegerField('ID склада', null=True, blank=True)
    RESERVE_ID = models.PositiveIntegerField('ID резерва', null=True, blank=True)
    DATE_RESERVE_END = models.CharField('Дата истечения резерва', max_length=256, null=True, blank=True)
    RESERVE_QUANTITY = models.DecimalField('Количество в резерве', max_digits=12, decimal_places=2, null=True,
                                           blank=True)
    PORTAL = models.ForeignKey(Portals, verbose_name='Портал', on_delete=models.CASCADE)
    ####################################################################################
    PACKAGE = models.ForeignKey('Package', verbose_name='Упаковка', on_delete=models.PROTECT,
                                related_name='package_productrows', null=True, blank=True)
    QUANTITY_PACKAGES = models.PositiveIntegerField('Количество упаковок', null=True, blank=True)
    QUANTITY_PALLETS = models.DecimalField('Количество паллет', max_digits=12, decimal_places=2, null=True, blank=True)
    TONNAGE = models.DecimalField('Тоннаж заказа', max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Товарная позиция ID {self.PRODUCTROW_ID} NAME {self.PRODUCT_NAME}'

    class Meta:
        verbose_name = 'Товарная позиция'
        verbose_name_plural = 'Товарные позиции'
        unique_together = ['PRODUCTROW_ID', 'PORTAL']
        indexes = [
            models.Index(fields=['PRODUCTROW_ID', 'PORTAL'], name='PRODUCTROW_ID_PORTAL_index')
        ]


class Entity(CreatedModel):
    """Модель для хранения параметров сущности-объекта Б24."""
    general_number = models.CharField(
        verbose_name='Основная часть заводского номера',
        max_length=200,
        null=True,
        blank=True,
    )
    last_factory_number = models.PositiveIntegerField(
        verbose_name='Последний заводской номер',
        default=0,
    )
    portal = models.ForeignKey(
        Portals,
        verbose_name='Портал',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Responsible(CreatedModel):
    """Модель для хранения ответственных сотрудников из Б24."""
    id_b24 = models.PositiveIntegerField(
        verbose_name='ID в Битрикс24',
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        blank=True,
        null=True,
    )
    position = models.CharField(
        verbose_name='Должность',
        max_length=255,
        blank=True,
        null=True,
    )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Ответственный'
        verbose_name_plural = 'Ответственные'


class Package(CreatedModel):
    """Модель Упаковки."""
    ACTIVE = models.BooleanField('Активность', default=True)
    NAME = models.CharField('Наименование', max_length=255, unique=True)
    WEIGHT = models.DecimalField('Вес', max_digits=13, decimal_places=3)
    QUANTITY_JARS = models.PositiveIntegerField('Количество банок')
    QUANTITY_ON_PALLET = models.PositiveIntegerField('Количество на паллете')
    WEIGHT_BRUTTO = models.DecimalField('Вес брутто паллета', max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.NAME}'

    class Meta:
        verbose_name = 'Упаковка'
        verbose_name_plural = 'Упаковки'
