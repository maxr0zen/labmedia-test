from datetime import datetime, timezone, timedelta
from django.core.management.base import BaseCommand
from apps.clients.models import Client
from apps.payments.models import Payment


TEST_CLIENTS = [
    {'id': 1, 'first_name': 'Ivan', 'last_name': 'Ivanov', 'country': 'Russia'},
    {'id': 2, 'first_name': 'Alexey', 'last_name': 'Smirnov', 'country': 'Russia'},
    {'id': 3, 'first_name': 'Sergey', 'last_name': 'Sidorov', 'country': 'USA'},
    {'id': 4, 'first_name': 'Dmitry', 'last_name': 'Petrov', 'country': 'USA'},
    {'id': 5, 'first_name': 'Oleg', 'last_name': 'Kolovin', 'country': 'Germany'},
]

TZ_PLUS_3 = timezone(timedelta(hours=3))

TEST_PAYMENTS = [
    {'id': 1, 'payer_id': 5, 'amount': '100.00', 'percent': 13, 'pay_date': datetime(2018, 8, 11, 10, 37, 50, tzinfo=TZ_PLUS_3)},
    {'id': 2, 'payer_id': 2, 'amount': '130.53', 'percent': 18, 'pay_date': datetime(2018, 8, 15, 15, 32, 43, tzinfo=TZ_PLUS_3)},
    {'id': 3, 'payer_id': 4, 'amount': '55.11', 'percent': 13, 'pay_date': datetime(2018, 9, 1, 9, 30, 35, tzinfo=TZ_PLUS_3)},
    {'id': 4, 'payer_id': 1, 'amount': '67.27', 'percent': 13, 'pay_date': datetime(2018, 9, 4, 19, 25, 11, tzinfo=TZ_PLUS_3)},
    {'id': 5, 'payer_id': 3, 'amount': '143.74', 'percent': 22, 'pay_date': datetime(2018, 9, 11, 11, 32, 59, tzinfo=TZ_PLUS_3)},
]


class Command(BaseCommand):
    help = 'Seed database with exact test data from assignment'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        Payment.objects.all().delete()
        Client.objects.all().delete()

        self.stdout.write('Creating test clients...')
        for data in TEST_CLIENTS:
            Client.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(TEST_CLIENTS)} clients'))

        self.stdout.write('Creating test payments...')
        for data in TEST_PAYMENTS:
            Payment.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(TEST_PAYMENTS)} payments'))
