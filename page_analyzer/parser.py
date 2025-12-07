from bs4 import BeautifulSoup


def get_data(content: str) -> dict:
    soup = BeautifulSoup(content, 'html.parser')
    data = {}
    
    # Извлекаем title
    title = soup.title.string if soup.title else None
    data['title'] = title[:255] if title else ''
    
    # Извлекаем h1 (берем только первый)
    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text().strip() if h1_tag else None
    data['h1'] = h1[:255] if h1 else ''
    
    # Извлекаем meta description
    data['description'] = ''
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta:  
        description_content = meta.get('content', '')
        data['description'] = description_content.strip()[:255] if description_content else ''
    
    return data