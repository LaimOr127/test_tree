from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """Модель для хранения названий меню"""
    name = models.CharField('Название меню', max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для хранения пунктов меню"""
    menu = models.ForeignKey(
        Menu, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='Меню'
    )
    name = models.CharField('Название пункта', max_length=100)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Родительский пункт'
    )
    url = models.CharField('URL', max_length=255, blank=True)
    named_url = models.CharField('Named URL', max_length=255, blank=True)
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_url(self):
        if self.url:
            return self.url
        elif self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return '#'
        return '#'
