import socket
import urllib.request
from bs4 import BeautifulSoup


def main():
    host = '127.0.0.1'
    port = 53910

    s = socket.socket()
    s.bind((host, port))

    s.listen(10)
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:
        data = c.recv(1024).decode().lower()
        if not data:
            break
        print("from connected user: " + str(data))
        data = respond(data)
        print("sending: " + data)
        c.send(data.encode())
    c.close()


def respond(data):
    if a in data:
        data = get_summary_about_faculty(data[len(a):])
    elif b in data:
        data = get_full_info_about_faculty(data[len(b):])
    elif m in data:
        data = get_tutors_from_faculty(data[len(m):])
    elif d in data:
        data = get_info_about_tutor(data[len(d):])
    elif data == 'knock knock':
        data = 'Who\'s there?'
    else:
        data = wrong_command()
    return data

a = 'get summary about '
b = 'get full info about '
m = 'get tutors from '
d = 'get info about '


def parse_site(url):
    html_page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


'''
https://nnov.hse.ru/ba/ + 
se - програмная инженерия
ami - Прикладная маткматика и информатика
economics
math
bi
management
law
philology
ling
'''


def wrong_command():
    message = ('Wrong command. \n'
               'You can command the following\n'
               '* Get summary about [faculty]\n'
               '* Get full info about [faculty]\n'
               '* Get tutors from [faculty]\n'
               '* Get info about [tutor]\n'
               '________________________\n'
               'What exactly do you want?')
    return message


def get_summary_about_faculty(faculty):
    soup = parse_site('https://nnov.hse.ru/ba/%s' % faculty)
    s = soup.findAll('div', attrs={'class': 'main content'})
    for x in s:
        return x.text

groups = {('math', 'economics', 'philology', 'ling'): 'about', 'management': 'about_the_program',
          'bi': 'programm', ('se', 'ami'): 'Programma'}


def get_full_info_about_faculty(faculty):
    ref = None
    for f, reference in groups.items():
        if faculty in f:
            ref = reference
    soup = parse_site('https://nnov.hse.ru/ba/%s/%s' % (faculty, ref))
    s = soup.findAll('div', attrs={'class': 'post__text'})
    for x in s:
        return x.text


def get_tutors_from_faculty(faculty):
    profs = ''
    soup = parse_site('https://nnov.hse.ru/ba/%s/tutors' % faculty)
    s = soup.findAll('a')
    for x in s:
        if len(x.text.split()) == 3 and x.text == x.text.title():
            if len(profs) == 0:
                profs = profs + x.text
            else:
                profs = profs + ', ' + x.text
    return profs


# чтобы можно было найти информацию о любом преподавателе, необходимо знать его ID
# таким образом, информация про любого будет в одном формате
# разумеется, для нормальной работы нужно, чтобы словарь был полным

tutors = {'Уткина': '46748315', 'Малафеев': 'aumalafeev', 'Романова': '34959567', 'Дурандин': '196754678',
          'Бочкарев': '133908342', 'Баринова': '62835110', 'Зусман': '26487692', 'Цветкова': '35038112'}


def get_info_about_tutor(surname):
    tutor_id = None
    for sn, tutid in tutors.items():
        if sn == surname:
            tutor_id = tutid
    soup = parse_site('https://www.hse.ru/org/persons/%s' % tutor_id)
    s = soup.findAll('div', attrs={'class': 'main__inner main__inner_'})
    for x in s:
        return x.text

if __name__ == '__main__':
    main()
