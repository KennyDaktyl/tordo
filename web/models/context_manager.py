import datetime
from .advertisements import Advertisement


def ads_active(request):
    datetime_now = datetime.date.today()
    ctx = {"ads": Advertisement.objects.filter(
        date_start__lte=datetime_now,
        date_end__gte=datetime_now
        ).order_by("order")
    }
    return ctx
