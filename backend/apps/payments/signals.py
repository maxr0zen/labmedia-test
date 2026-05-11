from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.clients.models import Client
from .models import Payment


def broadcast_update(model_name, instance_id, action):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard_updates',
        {
            'type': 'model_update',
            'model': model_name,
            'action': action,
            'id': instance_id,
        }
    )


@receiver(post_save, sender=Client)
def client_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    broadcast_update('client', instance.id, action)


@receiver(post_delete, sender=Client)
def client_deleted(sender, instance, **kwargs):
    broadcast_update('client', instance.id, 'delete')


@receiver(post_save, sender=Payment)
def payment_saved(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    broadcast_update('payment', instance.id, action)


@receiver(post_delete, sender=Payment)
def payment_deleted(sender, instance, **kwargs):
    broadcast_update('payment', instance.id, 'delete')
