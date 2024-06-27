import csv
import json
from django.core.management.base import BaseCommand
from search_app.models import Restaurant, Dish

class Command(BaseCommand):
    help = 'Import restaurant data from CSV'

    def handle(self, *args, **kwargs):
        with open('restaurants_small.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) 

            for row in reader:
                restaurant_id = row[0]
                restaurant_name = row[1]
                location = row[2]
                menu_data = row[3]

                if not menu_data:
                    self.stdout.write(self.style.WARNING(f"Skipping restaurant {restaurant_name} due to empty menu field"))
                    continue

                try:
                    menu = json.loads(menu_data.replace("'", "\""))
                except json.JSONDecodeError as e:
                    self.stdout.write(self.style.ERROR(f"JSON decode error for restaurant {restaurant_name}: {e}"))
                    continue

                restaurant, created = Restaurant.objects.get_or_create(
                    name=restaurant_name,
                    location=location
                )

                for dish_name, price in menu.items():
                    Dish.objects.get_or_create(
                        restaurant=restaurant,
                        name=dish_name,
                        defaults={'price': price}
                    )

        self.stdout.write(self.style.SUCCESS('Data import completed!'))
