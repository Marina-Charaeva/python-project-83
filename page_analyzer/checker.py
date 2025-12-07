import requests
from requests.exceptions import RequestException
from .parser import get_data


def check_website(url):
    """
    Выполняет проверку сайта и возвращает данные для сохранения в БД
    """
    try:
        # Выполняем GET-запрос с таймаутом 
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Парсим HTML с помощью парсера
        check_data = get_data(response.text)
        check_data['status_code'] = response.status_code
        
        return check_data
        
    except requests.exceptions.HTTPError as e:
        # Обрабатываем HTTP ошибки (4xx, 5xx) 
        if hasattr(e.response, 'status_code') and 500 <= e.response.status_code <= 599:
            # Серверные ошибки 5xx - не создаем проверку 
            raise CheckError(f'Сервер ответил с ошибкой {e.response.status_code}')
        else:
            # Клиентские ошибки 4xx - все равно создаем проверку
            return {
                'status_code': e.response.status_code,
                'h1': '',
                'title': '',
                'description': ''
            }
            
    except RequestException as e:
        # Обрабатываем сетевые ошибки 
        raise CheckError('Не удалось подключиться к сайту')
    
    except Exception as e:
        # Обрабатываем все остальные ошибки
        raise CheckError('Произошла непредвиденная ошибка при проверке')


class CheckError(Exception):
    """Кастомное исключение для ошибок проверки"""
    pass