from django.db import models


class Country(models.Model):
    name = models.CharField(primary_key=True, max_length=255, verbose_name = 'Название')

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'

    def __str__(self):
        return str(self.name)


class City(models.Model):
    name = models.CharField(primary_key=True, max_length=255, verbose_name = 'Название')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name = 'Страна')
    
    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return str(self.name)