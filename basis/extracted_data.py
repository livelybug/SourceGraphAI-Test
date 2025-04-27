from bs4 import BeautifulSoup
import requests
import json

def scrape_url1():
    url = "https://perinim.github.io/projects/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    projects = []
    
    for project in soup.find_all('div', class_='project'):
        title = project.find('h2').text.strip() if project.find('h2') else ''
        description = project.find('p').text.strip() if project.find('p') else ''
        
        projects.append({
            'title': title,
            'description': description
        })
    
    return projects

def main():
    projects = scrape_url1()
    print(json.dumps(projects, indent=2))

if __name__ == '__main__':
    main()