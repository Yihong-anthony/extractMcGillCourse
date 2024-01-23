"""
Programmer: Yihong Li
Created   : 2024/01/23
Purpose   : Extract course code, course name and course credit from
            from McGill ecalendar-
            'https://www.mcgill.ca/study/2023-2024/courses/search'.
            Then, put all these information into course.csv file

"""
import requests
import re


from bs4 import BeautifulSoup

url = 'https://www.mcgill.ca/study/2023-2024/courses/search'
file = open('text.txt', 'w')
for i in range(531):
    page = requests.get(url + "?page=" + str(i))

    info = BeautifulSoup(page.text, 'html.parser')
    courses = info.find_all('div', class_=
    'views-field views-field-field-course-title-long')
    for course in courses:
        file.write(str(course))
        file.write('\n')

file.close()

file = open('text.txt', 'r')
file1 = open('course.csv', 'w')

courseList = []
for line in file:
    if line[0:2] == '<d':
        courseList.append(line)
    else:
        courseList[-1] += line
print(courseList[0], courseList[1])

for course in courseList:
    ## remove the title
    courseInfo = course.removeprefix(
        '<div class="views-field views-field-field-course-'
        'title-long"> <h4 class="field-content"><a href="/'
        'study/2023-2024/courses/')
    courseInfo = re.sub(r'^.*?>', '>', courseInfo)

    ## remove the prefix and suffix
    courseInfo = courseInfo.rstrip('</a></h4> </div>\n').lstrip('>')
    courseDetail = courseInfo.split() ## split the courseInfo into words
    courseCode = courseDetail[0] + courseDetail[1]
    if courseDetail[-2][0] == '(':
        courseCredit = courseDetail[-2][1:]
        courseDescription = \
            ' '.join([courseDetail[i] for i in range(2,len(courseDetail) -2)])
    else:
        courseCredit = 'N/A'
        courseDescription = \
            ' '.join([courseDetail[i] for i in range(2,len(courseDetail))])

    file1.write((courseCode +',' + courseDescription + ',' + courseCredit+ '\n'))
file.close()
file1.close()
