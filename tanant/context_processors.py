from .models import Tanant

def tenant_broker_processor(request):
    has_broker = False
    if request.user.is_authenticated:
        try:
            tenant = Tanant.objects.get(user=request.user)
            has_broker = tenant.broker is not None
        except Tanant.DoesNotExist:
            pass
        except Tanant.MultipleObjectsReturned:
            pass
    return {'has_broker': has_broker}
