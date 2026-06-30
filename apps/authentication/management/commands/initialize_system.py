"""
Initialize the system with default data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from apps.authentication.models import Role, EnterprisePermission, PermissionCategory
from apps.common.models import Company, Branch, FeatureFlag

User = get_user_model()


class Command(BaseCommand):
    """Initialize the system with default data."""
    help = 'Initialize the system with default data'

    def handle(self, *args, **options):
        self.stdout.write('Initializing system...')

        # Create default company
        company, created = Company.objects.get_or_create(
            name='FabricERP Default Company',
            defaults={
                'legal_name': 'FabricERP Solutions',
                'tax_id': '0000000000',
                'commercial_register': '0000000',
                'industry': 'textile',
                'country': 'Egypt',
                'currency': 'EGP',
                'is_active': True,
                'is_verified': True,
                'subscription_status': 'active',
            }
        )
        self.stdout.write(f'{"Created" if created else "Found"} company: {company.name}')

        # Create default branch
        branch, created = Branch.objects.get_or_create(
            company=company,
            code='HQ',
            defaults={
                'name': 'Headquarters',
                'branch_type': 'hq',
                'is_headquarters': True,
                'is_active': True,
                'country': 'Egypt',
            }
        )
        self.stdout.write(f'{"Created" if created else "Found"} branch: {branch.name}')

        # Create permission categories
        categories = [
            {'name': 'Authentication', 'code': 'auth', 'description': 'Authentication and user management', 'is_system': True},
            {'name': 'Company', 'code': 'company', 'description': 'Company and branch management', 'is_system': True},
            {'name': 'Settings', 'code': 'settings', 'description': 'System settings', 'is_system': True},
            {'name': 'Accounting', 'code': 'accounting', 'description': 'Accounting module', 'is_system': True},
            {'name': 'Inventory', 'code': 'inventory', 'description': 'Inventory management', 'is_system': True},
            {'name': 'Sales', 'code': 'sales', 'description': 'Sales management', 'is_system': True},
            {'name': 'Purchasing', 'code': 'purchasing', 'description': 'Purchasing management', 'is_system': True},
            {'name': 'HR', 'code': 'hr', 'description': 'Human resources', 'is_system': True},
        ]

        for cat_data in categories:
            category, created = PermissionCategory.objects.get_or_create(
                code=cat_data['code'],
                defaults=cat_data
            )
            self.stdout.write(f'{"Created" if created else "Found"} category: {category.name}')

        # Create system permissions
        EnterprisePermission.create_system_permissions()
        self.stdout.write('Created system permissions')

        # Create system roles
        Role.create_system_roles()
        self.stdout.write('Created system roles')

        # Create superuser if none exists
        admin_username = getattr(settings, 'ADMIN_USERNAME', 'admin')
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@fabricerp.com')
        admin_password = getattr(settings, 'ADMIN_PASSWORD', 'Admin123!@#')

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=admin_username,
                full_name='System Administrator',
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(f'Created admin superuser: {admin_username}')
        else:
            self.stdout.write('Superuser already exists')

        # Create feature flags
        flags = [
            {
                'code': 'multi_company',
                'name': 'Multi-Company Support',
                'module': 'system',
                'description': 'Enable multi-company features',
                'status': 'enabled',
            },
            {
                'code': 'multi_branch',
                'name': 'Multi-Branch Support',
                'module': 'system',
                'description': 'Enable multi-branch features',
                'status': 'enabled',
            },
            {
                'code': 'audit_logging',
                'name': 'Audit Logging',
                'module': 'system',
                'description': 'Enable detailed audit logging',
                'status': 'enabled',
            },
        ]

        for flag_data in flags:
            flag, created = FeatureFlag.objects.get_or_create(
                code=flag_data['code'],
                defaults=flag_data
            )
            self.stdout.write(f'{"Created" if created else "Found"} feature flag: {flag.code}')

        self.stdout.write(self.style.SUCCESS('System initialized successfully!'))