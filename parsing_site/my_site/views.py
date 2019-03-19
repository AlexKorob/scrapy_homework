from django.shortcuts import render
from django.views import View
from .models import WarehouseItem, Image, Size
from django.http import HttpResponse, JsonResponse
from scrapy.utils.project import get_project_settings
from django.core.serializers import serialize
import redis
import json


redis_connect = redis.Redis(host='localhost', port=6379)


class Index(View):
    def get(self, request):
        if request.GET.get("get_data", ""):
            url = request.GET["url"]
            excludes = json.loads(request.GET["excludes"])
            items = {}

            for item in WarehouseItem.objects.filter(url=url).exclude(id__in=excludes):
                images = [img_url.url for img_url in Image.objects.filter(item=item)]
                sizes = [size.size for size in item.sizes.all()]
                items[item.id] = {"title": item.title,
                                  "company": item.company,
                                  "category": item.category,
                                  "images": images,
                                  "price": item.price,
                                  "sizes": sizes,
                                  "description" : item.description,}

            return JsonResponse(items)
        return render(request, "my_site/index.html")

    def post(self, request):
        url = request.POST["url"]
        error = self.validate_url(url)

        if error:
            return HttpResponse(error)

        redis_connect.lpush('warehouse:start_urls', url)
        return HttpResponse("success")

    def validate_url(self, url):
        error = ""
        split_url = url.split("/")
        if not url:
            error = "Поле не может быть пустым"
        elif (split_url[2] != "www.barneyswarehouse.com") and (split_url[2] != "barneyswarehouse.com"):

            error = "Парсер работает только с доменом barneyswarehouse.com"
        elif split_url[0] != "https:":
            error = "Url должен начинаться с https"

        if error:
            return error
        return False
