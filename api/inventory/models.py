from django.db import models

class Status(models.IntegerChoices):
    """
    状態
    """
    SYNC = 0, '同期'
    ASYNC_UNPROCESSED = 1, '非同期_未処理'
    ASYNC_PROCESSED = 2, '非同期_処理済'

class Product(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=100, verbose_name='商品名')
    price = models.IntegerField(verbose_name='価格')
    description = models.TextField(verbose_name='商品説明', null=True, blank=True)

    class Meta:
        db_table = 'product'
        verbose_name = '商品'

class Purchase(models.Model):
    """
    仕入
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    purchase_date = models.DateTimeField(verbose_name='仕入日時')

    class Meta:
        db_table = 'purchase'
        verbose_name = '仕入'

class SalesFile(models.Model):
    """
    売上ファイル
    """
    file_name = models.CharField(max_length=100, verbose_name='ファイル名')
    status = models.IntegerField(choices=Status.choices, verbose_name='状態')

    class Meta:
        verbose_name = '売上ファイル'
        db_table = 'sales_file'

class Sales(models.Model):
    """
    売上
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    sales_date = models.DateTimeField(verbose_name='売上日時')
    import_file = models.ForeignKey(
        SalesFile, on_delete=models.CASCADE, verbose_name='売上ファイルID')
    
    class Meta:
        db_table = 'sales'
        verbose_name = '売上'
