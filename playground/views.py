from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import Product, OrderItem, Customer, Order, Collection
from tags.models import TaggedItem
# Create your views here.
# request -> response
# request handler
def say_hello(request):
    #Pull data from DB
    #Transofmr Data
    #Send email 
    # return HttpResponse('Hello World')
    # x = calculate()

    # query_set = Product.objects.all() -> returns query_set
    # query_set.filter().filter().order_by()
    # product = Product.objects.filter(pk=0).exists()

    queryset = Product.objects.filter(unit_price__gt=20)
    queryset2 = Product.objects.filter(unit_price__range = (20,30))
    queryset3 = Product.objects.filter(collection__id__range = (1,2,3))
    queryset4 = Product.objects.filter(title__icontains='coffee')
    queryset5 = Product.objects.filter(title__startswith='coffee')
    queryset6 = Product.objects.filter(last_update__year=2021)
    queryset7 = Product.objects.filter(description__isnull=True)
    
    #Producs: inventory < 10 and price < 20
    queryset8 = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    queryset9 = Product.objects.filter(inventory__lt=20).filter(unit_price__lt=20)

    #Q Class
    queryset10 = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    queryset11 = Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))
    queryset11 = Product.objects.filter(~Q(inventory=9))
    queryset12 = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    # list(query_set)
    # query_set[0:5]
    
    # for product in query_set:
    #     print(product)

    #F Objects 

    queryset13 = Product.objects.filter(inventory=F('unit_price'))
    queryset14 = Product.objects.filter(inventory=F('collection__id'))

    #Sorting Data
    queryset15 = Product.objects.order_by('unit_price', '-title')
    queryset16 = Product.objects.order_by('unit_price', '-title').reverse() #This will reverse direction for sort. 
    queryset17 = Product.objects.filter(collection__id=1).order_by('unit_price')
    product = Product.objects.order_by('unit_price')[0] #Accessing first item, from queryset to object
    product2 = Product.objects.earliest('unit_price')
    product3 = Product.objects.latest('unit_price')
    
    #Limiting Results
    queryset18 = Product.objects.all()[:5]

    #Selecting fields to query 
    queryset19 = Product.objects.values('id', 'title', 'collection__collection_name')
    queryset20 = Product.objects.values_list('id', 'title', 'collection__collection_name')

    """
    Select products that have been ordered and sort them by title
    """
    
    queryset21 = Product.objects.filter(
        id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    queryset22 = Product.objects.only('id', 'title')
    
    queryset23 = Product.objects.select_related('collection').all()

    queryset24 = Product.objects.prefetch_related('promotions').all()

    queryset25 = Product.objects.prefetch_related('promotions').select_related('collection').all()

    result = Product.objects.filter(collection__id=1).aggregate(count = Count('id'), min_price=Min('unit_price'))

    queryset26 = Customer.objects.annotate(is_new=Value(True))
    queryset27 = Customer.objects.annotate(new_id=F('id') + 1)
    queryset28 = Customer.objects.annotate(
        full_name=Func(F('given_name'), Value(' '),
                        F('last_name'), function='CONCAT')
    )
    queryset29 = Customer.objects.annotate(
        full_name=Concat('given_name', Value(' '), 'last_name')
    )
    queryset30 = Customer.objects.annotate(
        orders_count=Count('order')
    )
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset31 = Product.objects.annotate(
        discounted_price=discounted_price
    )

    TaggedItem.objects.get_tags_for(Product, 1)

    #Creating objects
    collection = Collection()
    collection.collection_name = 'Video Games'
    collection.featured_product = Product(pk=1)
    # collection.featured_product_id = 1
    collection.save()

    # collection = Collection.objects.create(collection_name='Video Games', featured_product_id=1)

    #Updating objects 
    collection = Collection(pk=11)
    collection.collection_name='Games'
    collection.featured_product = None
    collection.save()

    collection = Collection.objects.get(pk=11)
    collection.featured_product= Product(pk=1)
    collection.save()

    #For performance issues
    Collection.objects.filter(pk=11).update(featured_product=None)

    # #Deleting Objects
    # collection = Collection(pk=11)
    # collection.delete()

    # #Multiple
    # Collection.objects.filter(id__gt=5).delete()

  

    """
    Transcations - Multiple changes to database in an atomic way. Changes should 
    be saved together
    if one fails all should roll back safely. 
    """

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    #Executing Raw SQL Queries
    queryset32 = Product.objects.raw('SELECT * FROM store_product')


    # with connection.cursor() as cursor:
    #     cursor.execute()
    #     cursor.callproc('get_customer', [1, 2, 'a'])

    return render(request, 'hello.html', {'name' : 'Nistha', 'tags' : list(queryset32)})
 