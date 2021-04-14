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
                .join([str(lesson) for lesson in self.lessons])

@dataclass
class Lesson:
    period: tuple
    title: str
    teacher: str
    classroom: str

    def __str__(self):
        return f'   <b>{self.period[0]} : {self.period[1]}</b> В аудитории {self.classroom} \n {self.title} ({self.teacher})'


def parse_lesson(soup: BeautifulSoup) -> Lesson:
    lesson_name, teacher = soup\
        .find('td', attrs={'class': 'lesson_td'})\
        .findAll('div')

    period = soup.find('span').text

    return Lesson(
        period=(period[:int(len(period) / 2)], period[int(len(period) / 2):]),
        title=lesson_name.text,
        teacher=teacher.text,
        classroom=soup.find('div', attrs={'class': 'place'}).text
    )


def parse_weekday(soup: BeautifulSoup) -> WeekDay:
    return WeekDay(
        title=soup.find('p').text,
        lessons=list(map(
            parse_lesson,
            soup.findAll('tr', attrs={'class': 'period-tr'})
        )),
    )


def parse(contents):
    soup = BeautifulSoup(contents, 'lxml')

    return list(map(parse_weekday, soup.findAll('div', attrs={'class': 'weekday-div'})))

