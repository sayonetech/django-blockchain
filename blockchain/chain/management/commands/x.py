from django.core.management import BaseCommand
from chain.models import Peer, Transactions

__author__ = 'sayone'


class Command(BaseCommand):

    def handle(self, *args, **options):
        x = Peer.objects.latest('id')
        x.mine_block('first', 'agdfelksuygdflsergflserfglhsebrlgfvsZDgfvsDfzsfcSZfvdszegdfv')
        print(x)