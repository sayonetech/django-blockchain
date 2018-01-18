from django.contrib import admin
from chain.models import *

# Register your models here.
admin.site.register(Block)
admin.site.register(Chain)
admin.site.register(Peer)
admin.site.register(Transactions)