from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=256,
                             verbose_name='Заголовок'
                             )  # , blank=False, null=False
    description = models.TextField(verbose_name='Описание')
    # blank=False, null=False
    slug = models.SlugField(
        # max_length=256, blank=False, null=False,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    is_published = models.BooleanField(
        default=True,
        # null=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',)
    created_at = models.DateTimeField(
        auto_now_add=True,
        # blank=False, null=False
        verbose_name='Добавлено'
    )

    def __str__(self):
        return f"{self.slug}: {self.title}: {self.description[:32]}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название места'
                            )  # blank=False, null=False
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    # , null=False
    created_at = models.DateTimeField(
        auto_now_add=True,
        # blank=False,
        # null=False
        verbose_name='Добавлено'
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(models.Model):
    title = models.CharField(max_length=256,
                             verbose_name='Заголовок'
                             )  # , blank=False, null=False
    text = models.TextField(
        verbose_name='Текст'
    )  # blank=False, null=False
    pub_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        # blank=False,
        # null=False
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем '
                  '— можно делать отложенные публикации.')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        # blank=False,
        null=False,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        # blank=True,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name='Категория'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    # , null=False
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    # , blank=False, null=False

    image = models.ImageField(
        "Картинка",
        upload_to=".media",

        blank=True,
        null=True,
    )

    def get_comment_count(self):
        return self.comment_set.count()

    @property
    def comment_count(self):
        return self.get_comment_count()

    def __str__(self):
        return f"{self.title} : {self.text[:32]} by {self.author}"

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

class Comment(models.Model):
    text = models.TextField(
        "Комментарий",
        blank=False,
        null=False,

    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        verbose_name="Автор",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Публикация"
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'