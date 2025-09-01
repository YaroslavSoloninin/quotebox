from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Source(models.Model):
    CHOICES = (
        ('book', 'Книга'),
        ('movie', 'Фильм'),
    )
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    type = models.CharField(choices=CHOICES)

    def __str__(self):
        return self.name


class Quote(models.Model):
    WEIGHT_CHOICES = (
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий')
    )
    text = models.TextField(unique=True)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='quotes',
    )
    weight = models.PositiveSmallIntegerField(
        choices=WEIGHT_CHOICES,
        default=1,
    )
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def clean(self):
        if not self.pk and self.source.quotes.count() >= 3:
            raise ValidationError('У одного источника не может быть больше трёх цитат.')

    def __str__(self):
        return f"{self.text[:30]}..."


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Лайк'),
        (-1, 'Дизлайк')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name='votes',
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'quote')
