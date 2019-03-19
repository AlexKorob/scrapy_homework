from celery.task import task
from .models import WarehouseItem, Image, Size


@task(name='save_warehouse_item')
def save_warehouse_item(items):
    for item in items:
        saved_item = WarehouseItem.objects.get_or_create(category=item.get("category"),
                                                         company=item.get("company"),
                                                         title=item.get("title"),
                                                         price=item.get("price"),
                                                         description=item.get("description"),
                                                         url=item.get("url"))
        item_not_on_db = saved_item[1]
        saved_item = saved_item[0]

        if item_not_on_db:
            images = item.get("images")
            for img in images:
                Image.objects.create(url=img, item=saved_item)

            sizes = item.get("sizes")
            for size in sizes:
                s = Size.objects.get_or_create(size=size)[0]
                saved_item.sizes.add(s)
    #     return f"{item['title']} was created"
    # return f"{item['title']} on db"
