from django.db import models


class Warehouse(models.Model):
    category = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    images = models.ForeignKey("Image", on_delete=models.CASCADE, related_name="warehouses")
    sizes = models.ForeignKey("Size", on_delete=models.CASCADE, related_name="warehouses")
    price = models.CharField(max_length=50)
    description = models.TextField()


class Image(models.Model):
    url = models.CharField(max_length=200)


class Size(models.Model):
    size = models.CharField(max_length=10)
