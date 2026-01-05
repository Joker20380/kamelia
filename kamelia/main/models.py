import os
import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from .fields import WEBPField
from django_ckeditor_5.fields import CKEditor5Field
from model_utils import FieldTracker
from django.utils import timezone
from .mixins import OccupancyMixin



def image_folder(instance, filename):
    return "photos/{}.webp".format(uuid.uuid4().hex)


# ============================================================
# ТВОИ МОДЕЛИ (как есть)
# ============================================================

class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name="Раздел сайта", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section', kwargs={'section_slug': self.slug})

    class Meta:
        verbose_name = 'Раздел сайта'
        verbose_name_plural = 'Разделы сайта'
        ordering = ['id']


class CategoryNews(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'
        ordering = ['id']


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = CKEditor5Field(blank=True, verbose_name="Текст", config_name="extends")
    photo = WEBPField(verbose_name='фото 633x550px', upload_to=image_folder, blank=True, null=True)
    content2 = CKEditor5Field(blank=True, null=True, verbose_name="Текст2", config_name="extends")
    photo2 = WEBPField(verbose_name='фото2', upload_to=image_folder,  blank=True, null=True)
    photo3 = WEBPField(verbose_name="Фото№3", upload_to=image_folder, blank=True, null=True)
    content3 = CKEditor5Field(blank=True, null=True, verbose_name="Текст3", config_name="extends")
    photo4 = WEBPField(verbose_name="Фото№4", upload_to=image_folder, blank=True, null=True)
    photo5 = WEBPField(verbose_name="Фото№5", upload_to=image_folder, blank=True, null=True)
    content4 = CKEditor5Field(blank=True, null=True, verbose_name="Текст4", config_name="extends")
    time_create = models.DateTimeField(verbose_name="Дата и время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата и время обновления")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    tracker = FieldTracker(fields=['is_published'])
    cat = models.ForeignKey(CategoryNews, on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={'news_slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['time_create', 'title']


class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = CKEditor5Field(blank=True, verbose_name="Текст")
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, verbose_name="Цена")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True, null=True)
    photo2 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото2", blank=True, null=True)
    photo3 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото3", blank=True, null=True)
    photo4 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото4", blank=True, null=True)
    photo5 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото5", blank=True, null=True)
    photo6 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото6", blank=True, null=True)
    time_create = models.DateTimeField(verbose_name="Дата и время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата и время обновления")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    number_of_employees = models.IntegerField(verbose_name="Количество сотрудников", default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services', kwargs={'services_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = [['title', 'slug']]
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True)  # Активна ли подписка
    unsubscribe_token = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Токен для отписки
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подписчика'
        verbose_name_plural = 'Подписчики'
        ordering = ['email']

    def __str__(self):
        return self.email


class ContactGroup(models.Model):
    """Группа контактов (например, Администрация, Филиал)"""
    name = models.CharField(max_length=100, verbose_name="Название группы")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Группа контактов"
        verbose_name_plural = "Группы контактов"
        ordering = ['order']

    def __str__(self):
        return self.name


class Contact(models.Model):
    """Конкретный контакт"""
    group = models.ForeignKey(
        ContactGroup,
        on_delete=models.CASCADE,
        verbose_name="Группа",
        related_name='contacts'
    )
    name = models.CharField(max_length=100, verbose_name="Название")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    is_main = models.BooleanField(default=False, verbose_name="Основной контакт")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ['order']

    def __str__(self):
        return f"{self.group}: {self.name}"


class ContactRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    contact = models.ForeignKey(
        'Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Контактное лицо"
    )

    class Meta:
        verbose_name = "Запрос на контакт"
        verbose_name_plural = "Запросы на контакт"
        ordering = ['-created_at']

    def __str__(self):
        contact_name = self.contact.name if self.contact else "Общий запрос"
        return f"{self.name} → {contact_name} ({self.created_at:%d.%m.%Y})"


# ============================================================
# ГОСТИНИЦА / НОМЕРА (НОВОЕ)
# ============================================================

def room_image_folder(instance, filename):
    # WEBPField сам сконвертит, здесь просто уникальное имя
    return "hotel/rooms/{}.webp".format(uuid.uuid4().hex)


class RoomCategory(models.Model):
    """
    Категория/тип номера (Стандарт, Люкс, Апартаменты).
    Отдельный справочник, чтобы делать страницы типа /rooms/lyuks/
    """
    title = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = CKEditor5Field(blank=True, verbose_name="Описание", config_name="extends")

    # “типовые” параметры (можно переопределять в Room)
    default_capacity = models.IntegerField(verbose_name="Вместимость по умолчанию", default=2)
    default_beds = models.CharField(max_length=120, verbose_name="Кровати по умолчанию", blank=True)

    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # под себя: rooms_category / room_category
        return reverse('room_category', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"
        ordering = ['order', 'id']


class RoomAmenity(models.Model):
    """
    Удобства номера (Wi-Fi, кондиционер, парковка, завтрак и т.д.)
    """
    title = models.CharField(max_length=150, verbose_name="Удобство", unique=True)
    icon = models.CharField(max_length=80, verbose_name="Иконка (fa/bi)", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"
        ordering = ['order', 'title']


class Room(models.Model):
    """
    Конкретный номер: 101, 202A и т.п.
    """
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_MAINTENANCE = "maintenance"

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "Активен"),
        (STATUS_INACTIVE, "Скрыт"),
        (STATUS_MAINTENANCE, "На обслуживании"),
    )

    title = models.CharField(max_length=255, verbose_name="Название (витрина)")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    number = models.CharField(max_length=30, verbose_name="Номер (например 101)", unique=True)
    category = models.ForeignKey(
        RoomCategory,
        on_delete=models.PROTECT,
        verbose_name="Категория номера",
        related_name="rooms"
    )

    content = CKEditor5Field(blank=True, verbose_name="Описание", config_name="extends")

    # характеристики
    floor = models.IntegerField(verbose_name="Этаж", blank=True, null=True)
    area_m2 = models.DecimalField(verbose_name="Площадь (м²)", max_digits=7, decimal_places=2, blank=True, null=True)

    capacity = models.IntegerField(verbose_name="Вместимость", default=2)
    beds = models.CharField(max_length=120, verbose_name="Кровати", blank=True)

    amenities = models.ManyToManyField(
        RoomAmenity,
        verbose_name="Удобства",
        blank=True,
        related_name="rooms"
    )

    # цена
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, verbose_name="Цена за ночь")
    currency = models.CharField(max_length=3, verbose_name="Валюта", default="RUB")

    # правила времени
    check_in_from = models.TimeField(verbose_name="Заезд с", blank=True, null=True)
    check_out_to = models.TimeField(verbose_name="Выезд до", blank=True, null=True)

    # публикация/статус
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE, verbose_name="Статус")

    # медиа — в твоём стиле WEBP (делаем 1 обложку + доп.фото)
    photo = WEBPField(verbose_name='Фото (обложка)', upload_to=room_image_folder, blank=True, null=True)
    photo2 = WEBPField(verbose_name='Фото2', upload_to=room_image_folder, blank=True, null=True)
    photo3 = WEBPField(verbose_name='Фото3', upload_to=room_image_folder, blank=True, null=True)
    photo4 = WEBPField(verbose_name='Фото4', upload_to=room_image_folder, blank=True, null=True)
    photo5 = WEBPField(verbose_name='Фото5', upload_to=room_image_folder, blank=True, null=True)

    time_create = models.DateTimeField(verbose_name="Дата и время создания", default=timezone.now)
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата и время обновления")

    tracker = FieldTracker(fields=['is_published', 'status'])

    def __str__(self):
        return f"{self.number} — {self.title}"

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            # slug будет человеко-читаемым и уникальным за счёт unique=True
            self.slug = slugify(f"{self.number}-{self.title}")
        # автоподстановка, если не заполнено руками
        if self.capacity is None and self.category_id:
            self.capacity = self.category.default_capacity
        if not self.beds and self.category_id:
            self.beds = self.category.default_beds
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ['number', 'id']


class RoomBooking(models.Model, OccupancyMixin):
    """
    Бронирование номера.
    """

    STATUS_NEW = "new"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = (
        (STATUS_NEW, "Новая"),
        (STATUS_CONFIRMED, "Подтверждена"),
        (STATUS_CANCELLED, "Отменена"),
        (STATUS_COMPLETED, "Завершена"),
    )

    # ─────────────────────────────────────────
    # Связи
    # ─────────────────────────────────────────
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        verbose_name="Номер",
        related_name="bookings"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )

    # ─────────────────────────────────────────
    # Даты проживания
    # ─────────────────────────────────────────
    date_from = models.DateField(verbose_name="Дата заезда")
    date_to = models.DateField(verbose_name="Дата выезда")

    # ─────────────────────────────────────────
    # Гости
    # ─────────────────────────────────────────
    adults = models.PositiveSmallIntegerField(
        verbose_name="Взрослые",
        default=2
    )

    children = models.PositiveSmallIntegerField(
        verbose_name="Дети",
        default=0
    )

    guests = models.PositiveSmallIntegerField(
        verbose_name="Всего гостей",
        default=2,
        help_text="Автоматически рассчитывается: взрослые + дети"
    )

    # ─────────────────────────────────────────
    # Контактные данные гостя
    # ─────────────────────────────────────────
    guest_name = models.CharField(
        max_length=120,
        verbose_name="Имя гостя"
    )

    guest_phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
        blank=True
    )

    guest_email = models.EmailField(
        verbose_name="Email",
        blank=True
    )

    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True
    )

    # ─────────────────────────────────────────
    # Финансы
    # ─────────────────────────────────────────
    total_price = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        default=0.00,
        verbose_name="Итого"
    )

    currency = models.CharField(
        max_length=3,
        verbose_name="Валюта",
        default="RUB"
    )

    # ─────────────────────────────────────────
    # Служебное
    # ─────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name="Статус"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено"
    )

    tracker = FieldTracker(fields=["status"])

    # ─────────────────────────────────────────
    # Логика
    # ─────────────────────────────────────────
    def save(self, *args, **kwargs):
        # всегда синхронизируем количество гостей
        self.guests = int(self.adults or 0) + int(self.children or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Бронь №{self.id or '—'} | "
            f"{self.room.number} | "
            f"{self.date_from} → {self.date_to} | "
            f"{self.guest_name}"
        )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["room", "date_from", "date_to"]),
            models.Index(fields=["status"]),
        ]

