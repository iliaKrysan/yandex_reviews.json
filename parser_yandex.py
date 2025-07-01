import requests
from bs4 import BeautifulSoup
import json
import time

# URL страницы отзывов вашей компании
url = "https://yandex.ru/maps/org/orekhovo_les/230761774916/reviews/?ll=40.810786%2C54.692079&utm_content=read-more&utm_medium=reviews&utm_source=maps-reviews-widget&z=10"

# Заголовки, чтобы выглядеть как обычный браузер
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def get_reviews():
    try:
        # Отправляем GET-запрос
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Ошибка доступа к странице: {response.status_code}")
            return []

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Контейнеры отзывов
        reviews_containers = soup.find_all('div', class_='business-review-view')
        
        if not reviews_containers:
            print("Не найдены отзывы на странице")
            print("HTML:", response.text[:2000])  # Показываем начало HTML для диагностики
            return []

        reviews_data = []

        for container in reviews_containers:
            # Текст отзыва
            text_elem = container.find('div', itemprop='reviewBody')
            review_text = text_elem.get_text(strip=True) if text_elem else ""

            # Оценка
            rating_elem = container.find('div', class_='business-rating-badge-view__stars')
            rating = len(rating_elem.find_all('svg')) if rating_elem else 0

            # Автор
            author_elem = container.find('span', itemprop='name')
            author = author_elem.get_text(strip=True) if author_elem else "Аноним"

            # Ссылка на аватар
            author_image_elem = container.find('meta', itemprop='image')
            author_image = author_image_elem['content'] if author_image_elem else ""
            
            # Дата
            date_elem = container.find('meta', itemprop='datePublished')
            date = date_elem['content'] if date_elem else ""

            # Добавляем в список
            reviews_data.append({
                "author": author,
                "rating": rating,
                "author_image": author_image,
                "text": review_text,
                "date": date
            })

        return reviews_data

    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# --- Основной запуск ---
if __name__ == "__main__":
    reviews = get_reviews()

    # Выводим результат
    print(json.dumps(reviews, ensure_ascii=False, indent=2))

    # Сохраняем в файл (опционально)
    with open('yandex_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    print(f"Сохранено {len(reviews)} отзывов в файл yandex_reviews.json")