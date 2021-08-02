#!/usr/bin/env python3
import datetime
import time
from PIL import Image
import pytesseract
import requests
import os
from dotenv import load_dotenv
load_dotenv(override=True)


def timer():
    now = datetime.datetime.now()
    while True:
        now = datetime.datetime.now()
        now_hour = int(now.hour)
        now_min = int(now.minute)
        target_hour = int(GRAB_HOUR)
        target_min = int(GRAB_MINUTE)
        if now_hour == target_hour and now_min == target_min:
            print(f"[ {now.hour} : {now.minute} ] Start to grab !!!!")
            break
        time.sleep(1)
        print(f"[ {now.hour} : {now.minute} ] It's not time yet. Target time is: [ {target_hour} : {target_min} ]")
        continue


def print_info():
    print('------------- Input Info -------------')
    print(f"""
    ID: {os.getenv('ID')}, \n
    BIRTH_YEAR: {os.getenv('BIRTH_YEAR')}, \n
    BIRTH_MONTH: {os.getenv('BIRTH_MONTH')}, \n
    BIRTH_DATE: {os.getenv('BIRTH_DATE')}, \n
    DOCTOR_NAME: {os.getenv('DOCTOR_NAME')}, \n
    CALENDAR_INDEX: {os.getenv('CALENDAR_INDEX')}, \n
    GRAB_HOUR: {os.getenv('GRAB_HOUR')}, \n
    GRAB_MINUTE: {os.getenv('GRAB_MINUTE')} \n
    DURANTION: {os.getenv('DURANTION')}, \n
    FREQUENCY: {os.getenv('FREQUENCY')}
    """)
    print('--------------------------------------')


def get_string_from_image():
    img = Image.open('image.png')
    result = int(pytesseract.image_to_string(img))
    return str(result)


def get_validate_photo():
    url = 'https://webreg.tpech.gov.tw/ValidateCode.aspx'
    data = requests.get(url, verify=False)
    with open("image.png", "wb") as fp:
        fp.write(data.content) #r.text is the binary data for the PNG returned by that php script


def check_book_success(id, year, month, day, doctor_name):
    print('Start to verify booking status')
    url = "https://webreg.tpech.gov.tw/RegOnline3_1.aspx"
    querystring = {"ChaId":"A103","tab":"3"}
    headers = { "Content-Type": "application/x-www-form-urlencoded"}
    payload = f"PAT_IDNO=rbPAT_ID&no={id}&yeartype=&y1={year}&m1={month}&d1={day}&TextBox1=1352&YRadio=on&PAT_NOTextBox=&Button1=%25E6%259F%25A5%25E8%25A9%25A2%25E6%258E%259B%25E8%2599%259F"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, verify=False)
    if response.status_code != 200:
        return False
    booking_stauts = False if (response.text.find('查無掛號資料!') != -1) else True
    docker_validate = False if (response.text.find(doctor_name) == -1) else True
    print(f"booking_stauts: {booking_stauts}, docker_validate: {docker_validate}")
    return True if booking_stauts and docker_validate else False
    


def make_an_appointment(doctor_name: str, index: str):
    url = "https://webreg.tpech.gov.tw/RegOnline1_3.aspx"

    querystring = {"ChaId":"A105","tab":"1","index":"1"}

    payload = ""
    headers = {
        "cookie": "TS0142a50e=019afc174eade5202277b6fada338e21f1c0dce6c469b25f07db927f078283879786e3d47b0db60c8329e5ffd0b05b639ed735b32565aa5c9251cce8d1c8195c54efb03891; ASP.NET_SessionId=ymb55zr0yayahf55lc5msrax",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)


def grab_vaccine():
    check_book_success(ID, BIRTH_YEAR, BIRTH_MONTH, BIRTH_DATE, DOCTOR_NAME)

if __name__ == '__main__':
    ID=os.getenv('ID')
    BIRTH_YEAR=os.getenv('BIRTH_YEAR')
    BIRTH_MONTH=os.getenv('BIRTH_MONTH')
    BIRTH_DATE=os.getenv('BIRTH_DATE')
    DOCTOR_NAME=os.getenv('DOCTOR_NAME')
    CALENDAR_INDEX=os.getenv('CALENDAR_INDEX')
    GRAB_HOUR=os.getenv('GRAB_HOUR')
    GRAB_MINUTE=os.getenv('GRAB_MINUTE')
    DURANTION=os.getenv('DURANTION')
    FREQUENCY=os.getenv('FREQUENCY')
    print_info()
    timer()

    # while True:
    if grab_vaccine():
        print("搶到啦")
        # break
        
    else:
        print("哭哭沒搶到")