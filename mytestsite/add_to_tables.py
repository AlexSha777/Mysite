#from django.conf import settings
#from apps import MoneyMoveConfig

#settings.configure(default_settings=MoneyMoveConfig, DEBUG=True)
import django
from models import MoneyMove, MoneySource, SpendingKind

if __name__ == '__main__':
    
    django.setup()
    all_entries = MoneySource.objects.all()
    print(all_entries)

