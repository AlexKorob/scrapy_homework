from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import redis

redis_connect = redis.Redis(host='localhost', port=6379, db=0)


class Index(View):
    def get(self, request):
        return render(request, "my_site/index.html")

    def post(self, request):
        url = "https://www.barneyswarehouse.com/category/men/clothing/activewear/N-1f3gneh"
        redis_connect.lpush('warehouse:start_urls {0}'.format(url), 1)
        return HttpResponse("success")
