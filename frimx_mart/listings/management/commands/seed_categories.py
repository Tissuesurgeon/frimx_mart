from django.core.management.base import BaseCommand
from listings.models import Category

class Command(BaseCommand):
    help = 'Seed categories for the marketplace'

    def handle(self, *args, **options):
        categories_data = [
            {'name': 'Fashion', 'icon': '👕', 'description': 'Clothing, shoes, accessories'},
            {'name': 'Electronics', 'icon': '📱', 'description': 'Phones, laptops, gadgets'},
            {'name': 'Computers & Tablets', 'icon': '💻', 'description': 'Laptops, desktops, tablets'},
            {'name': 'Mobile & Accessories', 'icon': '📱', 'description': 'Smartphones, cases, chargers'},
            {'name': 'Audio & Headphones', 'icon': '🎧', 'description': 'Headphones, speakers, audio equipment'},
            {'name': 'Cameras & Camcorders', 'icon': '📷', 'description': 'Cameras, lenses, accessories'},
            {'name': 'Gaming Equipment', 'icon': '🎮', 'description': 'Gaming consoles, accessories'},
            {'name': 'Home Appliances', 'icon': '🏠', 'description': 'Home and kitchen appliances'},
            {'name': 'Home & Garden', 'icon': '🏡', 'description': 'Furniture, decor, garden tools'},
            {'name': 'Vehicles', 'icon': '🚗', 'description': 'Cars, motorcycles, bikes'},
            {'name': 'Property', 'icon': '🏘️', 'description': 'Real estate listings'},
            {'name': 'Services', 'icon': '🛠️', 'description': 'Professional services'},
            {'name': 'Jobs', 'icon': '💼', 'description': 'Job listings'},
            {'name': 'Education', 'icon': '🎓', 'description': 'Courses, books, educational materials'},
            {'name': 'Sports', 'icon': '⚽', 'description': 'Sports equipment and gear'},
            {'name': 'Books', 'icon': '📚', 'description': 'Books and magazines'},
            {'name': 'Toys & Games', 'icon': '🧸', 'description': 'Toys and board games'},
            {'name': 'Health & Beauty', 'icon': '💄', 'description': 'Health and beauty products'},
            {'name': 'Other', 'icon': '📦', 'description': 'Miscellaneous items'},
        ]
        
        created_count = 0
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'description': cat_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} new categories!'))
