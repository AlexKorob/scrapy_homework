from django.db import models


class WarehouseItem(models.Model):
    category = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    sizes = models.ManyToManyField("Size", related_name="warehouses")
    price = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    url = models.SlugField(max_length=255)


class Image(models.Model):
    item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE, related_name="images")
    url = models.CharField(max_length=200)


class Size(models.Model):
    size = models.CharField(max_length=10)
