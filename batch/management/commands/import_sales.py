import pandas
from django.core.management.base import BaseCommand
from django.db import transaction

from api.inventory.models import Sales, SalesFile, Status

@transaction.atomic
def execute(download_history):
    entry = SalesFile.objects.select_for_update().get(pk=download_history.id)
    if entry.status != Status.ASYNC_UNPROCESSED:
        return
    
    filename = entry.file_name

    df = pandas.read_csv(filename)
    for _, row in df.iterrows():
        sales = Sales(product_id=row['product'], sales_date=row['date'],
                      quantity=row['quantity'], import_file=entry)
        sales.save()

        entry.status = Status.ASYNC_PROCESSED
        entry.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            download_hisotry = SalesFile.objects.filter(
                status=Status.ASYNC_UNPROCESSED).order_by('id').first()
            
            if download_hisotry is None:
                # 実行中に未処理以外になったば場合はスキップ
                break
            else:
                execute(download_hisotry)