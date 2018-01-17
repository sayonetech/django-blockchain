from django.core.management import BaseCommand
from chain.models import Transactions

class Command(BaseCommand):

    def handle(self, *args, **options):
       from faker import Faker
       fake = Faker()
       for _ in range(0, 20):
           transaction = Transactions.objects.create(sender=fake.name(), receiver=fake.name(), amount=fake.numerify())

