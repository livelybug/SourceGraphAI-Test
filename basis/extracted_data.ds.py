from bs4 import BeautifulSoup

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    projects = []
    
    for project_element in soup.find_all('div', class_='grid-item'):
        title_element = project_element.find('h4', class_='card-title')
        description_element = project_element.find('p', class_='card-text')
        
        title = title_element.text.strip() if title_element else ''
        description = description_element.text.strip() if description_element else ''
        
        if title or description:
            projects.append({
                'title': title,
                'description': description
            })
    
    return {'projects': projects}
