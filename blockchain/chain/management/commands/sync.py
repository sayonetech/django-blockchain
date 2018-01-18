from django.core.management import BaseCommand
from chain.models import Peer, Transactions, Block

__author__ = 'sayone'


class Command(BaseCommand):

    def handle(self, *args, **options):

        # transactions = Transactions.objects.filter(added_to_block=False).order_by('id')[0]
        # transactions.added_to_block = True
        # transactions.save()
        # transactions.__dict__.pop("added_to_block", 0)
        # transactions.__dict__.pop("_state", 0)
        # peer = Peer.objects.order_by('-id')[0]
        # peer.mine_block('first',  str(transactions.__dict__))
        for block in Block.objects.all():
             block.sync
