from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class WeekDay:
    title: str
    lessons: list

    def __str__(self):
        # return f'{self.title}\n' \
        #        + '\n'.join([str(lesson) for lesson in self.lessons])
        return f"<b>{self.title}</b>\n" + \
                '\n'.join([str(lesson) for lesson in self.lessons])


@dataclass
class Lesson:
    period: str
    title: str
    teacher: str
    place: str
    room: str
    week: str

    def __str__(self):
        return f'🕜 <b>{self.period}</b> <b> {self.week} </b>\n' \
               f'   {self.title} ({self.teacher}) \n' \
               f'   {self.room}  {self.place} \n'


def parse_lesson(soup: BeautifulSoup) -> Lesson:
    time = soup.find('td', attrs={'class': 'time'})
    period = time.find('span').text
    week = time.find('dt').text if time.find('dt') is not None else ''

    lesson = soup.find('td', attrs={'class': 'lesson'})
    title, teacher = lesson.find('dd'), lesson.find('b')

    classroom = soup.find('td', attrs={'class': 'room'})
    place, room = classroom.find('span'), classroom.find('dd')

    return Lesson(
        period=period,
        week=week,
        title=title.text,
        teacher=teacher.text.strip(),
        place=place.text,
        room=room.text
    )


def parse_weekday(soup: BeautifulSoup) -> WeekDay:
    return WeekDay(
        title=soup.find('th', attrs={'class': 'day'}).text,
        lessons=list(map(
            parse_lesson,
            filter(
                lambda s: len(s.contents) > 0,
                soup.findAll('tr')
            )
        )),
    )


def parse(contents):
    soup = BeautifulSoup(contents, 'lxml')

    return list(map(parse_weekday, soup.findAll('table', attrs={'class': 'rasp_tabl'})[1:]))

