from bs4 import BeautifulSoup as bs


def find_tags(response):
    soup = bs(response.text, 'html.parser')
    title = soup.title
    '''
    if title is None:
        title = ''
    else:
        title = title.text
    '''
    title = '' if not title else title.text
    h1 = soup.h1
    '''
    if h1 is None:
        h1 = ''
    else:
        h1 = h1.text
    '''
    h1 = '' if not h1 else h1.text
    description = soup.find('meta', attrs={'name': 'description'})
    '''
    if description is None:
        description = ''
    else:
        description = description['content']
    '''
    description = '' if not description else description['content']
    return {'title': title, 'h1': h1,
            'description': description}
