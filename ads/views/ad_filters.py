AD_FILTERS = {
    'tag': 'tags__name__contains',
    'cat': 'category__id',
    'text': 'name__icontains',
    'location': 'author__location__name__icontains',
    'price_from': 'price__gte',
    'price_to': 'price__lte',
}

# if r_get := request.GET.get("tag", None):
# ads_list = ads_list.filter(tags__name__contains=r_get)
#
# if r_get := request.GET.get("cat", None):
# ads_list = ads_list.filter(category__id=r_get)
#
# if r_get := request.GET.get("text", None):
# ads_list = ads_list.filter(name__icontains=r_get)
#
# if r_get := request.GET.get("location", None):
# ads_list = ads_list.filter(author__location__name__icontains=r_get)
#
# if r_get := request.GET.get("price_from", None):
# ads_list = ads_list.filter(price__gte=r_get)
#
# if r_get := request.GET.get("price_to", None):
# ads_list = ads_list.filter(price__lte=r_get)
