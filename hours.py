import sys
import xml.etree.cElementTree as xml
from xml.etree.ElementTree import Element, SubElement, ElementTree

def take_input():
    print ('\nYou can input your hours worked per session,\nI\'ll keep track of them for you')
    print ('Please pick a course from the following list?\n')
    course_options = [line.rstrip('\n') for line in open('list.txt')]
    for opt in course_options:
        print opt
    print '\n0. See logs'
    print '-1. exit()'
    ind = raw_input('\nYour choice: ')
    if int(ind) is 0:
        sn_t = 0
    elif int(ind) is -1:
        sys.exit()
    else:
        sn_t = raw_input('\nThis session time in hours: ')
    return ind, sn_t, course_options

def get_title(iindex, oopts):
    iindex = int(iindex)-1
    select = oopts[int(iindex)]
    tit = select[:0] + select[0 + 3:]
    return tit

def set_attributes(rroot, elem, ttitle, ssession_t):
    '''new course to add'''
    ccourse = SubElement(rroot, "att", course=ttitle, time=ssession_t)
    '''new time to add'''

running = 1
while(int(running) != -1):
    try:
        tree = ElementTree(file='db.xml')
        root = tree.getroot()

        '''take user's input'''
        index, session_t, course_opts = take_input()
        running = index
        if int(index) is 0:
            for e in root.iter():
                print e.get('course'), e.get('time')
        else:
            course_title = get_title(index, course_opts)

            i = 0
            '''updates hours instead of creating new or setting other attributes'''
            for c in root.iter():
                if c.get('course') == course_title:
                    timess = str(int(c.get('time')) + int(session_t))
                    root.remove(c)
                    elem_tmp = SubElement(root, "att", course=course_title, time=timess)
                    i = 1
                    break

            '''if there is new class then create new SubElement setting all its attributes'''
            if not i:
                course = Element('course')
                set_attributes(root, course, course_title, session_t)

            tree.write('db.xml')

            print 'Added: '+session_t+' hour(s) invested to ' + course_title

    except IOError as e:
        '''When there is no file created, create new file and set attributes'''
        i, time, opts = take_input()
        running = i
        froot = xml.Element('courses')
        fcourse = xml.Element('course')
        ftitle = get_title(i, opts)

        set_attributes(froot, fcourse, ftitle, time)

        tree = xml.ElementTree(froot)

        with open("db.xml", "w") as fh:
            tree.write(fh)

        print 'added '+time+' hours invested to ' + ftitle

    except:
        running = -1
        print '-debug-'
