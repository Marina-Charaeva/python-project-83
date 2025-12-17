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
        response.raise_for_status()  # Вызовет HTTPError для 4xx/5xx
        
        # Парсим HTML
        check_data = get_data(response.text)
        check_data['status_code'] = response.status_code
        
        return check_data
        
    except requests.exceptions.HTTPError as e:
        if hasattr(e.response, 'status_code'):
            status_code = e.response.status_code
            # 5xx ошибки - не создаем проверку
            if 500 <= status_code <= 599:
                raise CheckError('Произошла ошибка при проверке')
            else:
                # 4xx ошибки - все равно создаем проверку
                return {
                    'status_code': status_code,
                    'h1': '',
                    'title': '',
                    'description': ''
                }
        else:
            raise CheckError('Произошла ошибка при проверке')
            
    except RequestException:
        raise CheckError('Произошла ошибка при проверке')
    
    except Exception:
        raise CheckError('Произошла ошибка при проверке')


class CheckError(Exception):
    pass