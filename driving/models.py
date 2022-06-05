from django.db import models

# Create your models here.


class Src(models.Model):
    src = models.CharField('出発地', max_length=255)


class Dest(models.Model):
    name = models.CharField('名称', max_length=255)
    latitude = models.CharField('北緯', max_length=255)
    longitude = models.CharField('東経', max_length=255)
    address = models.CharField('所在地', max_length=255)


class geoCash(models.Model):
    src = models.CharField('出発地', max_length=255)
    latitude = models.CharField('北緯', max_length=255)
    longitude = models.CharField('東経', max_length=255)


class routeCash(models.Model):
    src = models.CharField('出発地', max_length=255)
    dest = models.CharField('目的地', max_length=255)
    highway = models.CharField('高速', max_length=255)
    localway = models.CharField('下道', max_length=255)
