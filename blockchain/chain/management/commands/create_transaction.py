from django.core.management import BaseCommand
from chain.models import Transactions, Peer

class Command(BaseCommand):

    def handle(self, *args, **options):
        from faker import Faker
        fake = Faker()
        transaction = Transactions.objects.create(sender=fake.name(), receiver=fake.name(), amount=fake.numerify())

        transactions = Transactions.objects.latest('id')
        transactions.added_to_block = True
        transactions.save()
        transactions.__dict__.pop("added_to_block", 0)
        transactions.__dict__.pop("_state", 0)
        peer = Peer.objects.order_by('-id')[0]
        peer.mine_block('second',  str(transactions.__dict__))
        peer.synchronize('second')