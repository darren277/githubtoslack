""""""
from bs4 import BeautifulSoup as bs
# Step 1 - Export full HTML: https://op.apphosting.services/projects/your-scrum-project/wiki/export.html

def fetch_toc_html(exported_html_file_path: str):
    file = exported_html_file_path
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = bs(html, 'html.parser')

    toc_html = soup.find('strong', text='Index by title').find_next('ul')

    toc_arr = []
    for li in toc_html.find_all('li'):
        a = li.find('a')
        toc_arr.append((a['href'].replace('#', ''), a.text))

    print(toc_arr)

    ## EXTRACT TEXT CONTENT IN BETWEEN ANCHOR TAGS ##
    anchors = soup.find_all('a', attrs={'name': True})

    sections = {}

    for i, anchor in enumerate(anchors):
        section_name = anchor['name']

        content = []
        sibling = anchor.find_next_sibling()

        while sibling and (sibling.name != 'a' or not sibling.has_attr('name')):
            content.append(sibling.text)
            sibling = sibling.find_next_sibling()

        sections[section_name] = '\n'.join(content).strip()

    for name, content in sections.items():
        print(f'SECTION: {name}')
        print(content)

    return toc_arr, sections
