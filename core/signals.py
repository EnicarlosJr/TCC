from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    username = settings.SUPERUSER_NAME
    email = settings.SUPERUSER_EMAIL
    password = settings.SUPERUSER_PASSWORD

    if not User.objects.filter(username=username).exists():
        print(f"✅ Criando superusuário: {username}")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"ℹ️ Superusuário '{username}' já existe.")
