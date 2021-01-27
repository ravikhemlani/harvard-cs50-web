from .models import Categories, WatchList


def message_processor(request):
    categories = Categories.objects.all()
    try:
        watchlist = WatchList.objects.get(user=request.user).items.all().count()
    except:
        watchlist = None
    return {"cat": categories, "num_watchlist": watchlist}
