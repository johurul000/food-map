from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from django.shortcuts import render
from .models import Restaurant
from django.http import JsonResponse
from Levenshtein import distance as levenshtein_distance
from .models import Dish

# Create your views here.

def search(request):
    query = request.GET.get('query')
    
    if query:
        if ' - ' in query:
            dish_name, restaurant_name = query.split(' - ', 1)
        else:
            dish_name = query
            restaurant_name = None
        
        dish_name = dish_name.strip().lower()

        dishes = Dish.objects.all()

        dishes_with_distance = [(dish, levenshtein_distance(dish.name.lower(), dish_name)) for dish in dishes]
        dishes_with_distance.sort(key=lambda x: x[1])

        best_matches = [dish for dish, distance in dishes_with_distance[:15]]

        for dish in best_matches:
            if not dish.image:
                image = fetch_image_url(dish.name)
                if image:
                    save_image_from_url(dish, image)


        best_match_ids = [dish.id for dish in best_matches]
        best_matches = Dish.objects.filter(id__in=best_match_ids)

    return render(request, 'search_app/search.html', {'best_matches': best_matches, 'dish_name': dish_name})


def fetch_image_url(query):
    access_key = 'Unsplash Access Key'
    url = f"https://api.unsplash.com/search/photos?page=1&query={query}&client_id={access_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']
    return None

def save_image_from_url(dish, image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            dish.image.save(f"{dish.name}.jpg", File(img_temp), save=True)
    except Exception as e:
        print(f"Error saving image for {dish.name}: {e}")


def home(request):
    return render(request, 'search_app/home.html')


def search_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        dishes = Dish.objects.all()
        suggestions = sorted(dishes, key=lambda dish: levenshtein_distance(dish.name.lower(), query.lower()))[:5]
        suggestions = [{'name': dish.name, 'restaurant': dish.restaurant.name} for dish in suggestions]
    else:
        suggestions = []

    return JsonResponse(suggestions, safe=False)


