"""
Create a superuser from command line.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """Create a superuser."""
    help = 'Create a superuser'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username')
        parser.add_argument('--email', type=str, required=True, help='Email')
        parser.add_argument('--password', type=str, required=True, help='Password')
        parser.add_argument('--full_name', type=str, help='Full name')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        full_name = options.get('full_name', username)

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists.'))
            return

        User.objects.create_superuser(
            username=username,
            full_name=full_name,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully!'))