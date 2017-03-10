# -*- coding: utf-8 -*-

import requests
import easygui
import json
import os
import time

#reading config file
config_file = open('config.json', 'r')
config_data = config_file.read()
config_file.close()
config_json = json.loads(config_data)


#configurations
check_frequency = config_json['check_frequency_in_mins']
user_info = config_json['user_info']
user_name = user_info['user_name']
password = user_info['password']
id = user_info['id']

#urls
base_url = "http://gezer1.bgu.ac.il/meser/"
entrance_file = 'entrance.php'
grades_file = 'crslist.php'
entrance_url = base_url + entrance_file
grades_url = base_url + grades_file

#parms
loginParams = {'uname': user_name, 'passwd': password, 'id' : id}
gradesParms = {'agree' : 'מסכים'}

#headres
gradesHeader = {'Referer' : entrance_url}

#counters
exam_notebooks = 0
grade_sheets = 0

#Checking for new grades:
while True:
    loginReq = requests.post(entrance_url, data = loginParams)
    loginReq.raise_for_status()
    gradesReq = requests.post(grades_url, headers = gradesHeader, data = gradesParms, cookies = loginReq.cookies)
    gradesReq.raise_for_status()
    lines = gradesReq.text.split(os.linesep)
    new_exam_notebooks = 0
    new_grade_sheets = 0
    for line in lines:
        if line.find('קובץ המחברת'.decode('UTF-8')) != -1:
    	    new_exam_notebooks = new_exam_notebooks + 1
        if line.find('קובץ שאלון/ציונים'.decode('UTF-8')) != -1:
    	    new_grade_sheets = new_grade_sheets + 1
    if exam_notebooks !=0 and exam_notebooks < new_exam_notebooks:
        print '\a'
        easygui.msgbox('New Exam notebook uploaded', 'Grades notifier')
    if grade_sheets !=0 and grade_sheets < new_grade_sheets:
        print '\a'
        easygui.msgbox('New Grade sheet uploaded', 'Grades notifier')
    exam_notebooks = new_exam_notebooks
    grade_sheets = new_grade_sheets
    time.sleep(check_frequency * 60)
			