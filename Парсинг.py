import requests
from bs4 import BeautifulSoup
import fake_useragent
import re


login_url = 'https://api.100points.ru/login'

email = 'sk@flash.info'
password = 'sk@flash.info'

session = requests.Session()

login_data = {
    'email': email,
    'password': password
}
header = {'user-agent': fake_useragent.UserAgent().random,
                  }

response = session.post(login_url, headers=header, data=login_data)


n = 1
links = []
is_next_page = None
dic = {}
parse_link = 'https://api.100points.ru/student_homework/index?status=passed&course_id=84&module_id=477&lesson_id=7017&group_id=1157'
with open("Students.txt", encoding='UTF-8') as file:
    for i in file:
        dic[i.rstrip()] = [0, 0]
        # dic[i.rstrip()] = 0
while not is_next_page:
    parse_link += f'&page={n}'
    response = session.get(parse_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    is_next_page = soup.find('li', id='example2_next').find('a').get('disabled')
    n += 1
    for a in soup.find_all('a', href=True):
        if re.match("https://api\.100points\.ru/student_homework/view/*", a['href']):
            response = session.get(a['href'])
            soup = BeautifulSoup(response.content, 'html.parser')
            label = soup.find('label', text=lambda text: text and text.startswith('Тестовая'))
            score = label.parent.text.replace(label.text, '').strip().split('/')
            print(score)
            student = soup.find('input', type="text").get('value')
            complexity = score[1] == '10'
            dic[student][complexity] = max(dic[student][complexity], int(score[0]))
            # dic[student] = max(dic[student], int(score[0]))
with open('Ans.txt', 'w') as file:
    for i in dic.values():
        # file.write(str(i))
        file.write('\t'.join(list(map(str, i))))
        file.write('\n')

