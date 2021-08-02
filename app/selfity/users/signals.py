from django.db.models.signals import post_save
from django.dispatch import receiver
from selfity.users.models import User
from selfity.sms.services import SmsService
from selfity.caches.utils import cache_instance
from selfity.users.serializers import UserPhoneSerializer
from selfity.caches.utils import get_cached_object


def send_message(user):
    sms_service = SmsService()
    response = sms_service.send_sms(user.phone_number, user.code)
    if response['statusCode'] == 200:
        cache_instance(
            instance=user,
            serializer=UserPhoneSerializer,
            cache_name='users'
        )


@receiver(post_save, sender=User)
def send_sms_code(sender, instance, **kwargs):
    send_message(instance)


"""@receiver(post_delete, sender=BlogPost)
def delete_cached_post(sender, instance, **kwargs):
    caches['blog_posts'].delete(instance.slug)"""