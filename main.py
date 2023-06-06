import pandas
import smtplib
import random
import datetime
import os

birthdays = pandas.read_csv("birthdays.csv")
birthday_dict = birthdays.to_dict(orient="records")

today = datetime.datetime.now()
now_str = str(today)
now_month = now_str[5:7]
now_day = now_str[8:10]
now_time = now_str[11:16]

for entry in birthday_dict:
    if str(entry["day"]).zfill(2) == now_day and str(entry["month"]).zfill(2) == now_month:
            person_name = entry["name"]
            person_email = entry["email"]

            dir = "letter_templates"
            file_name = random.choice(os.listdir(dir))
            path = os.path.join(dir, file_name)

            with open(path, "r") as letter_file:
                content = letter_file.read()
                named_content = content.replace("[NAME]", person_name )

            with open("credentials.txt", "r") as credential_file:
                credential_list = credential_file.readlines()
                user_id = credential_list[0][:-1]
                user_password = credential_list[1]

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=user_id, password=user_password)
                connection.sendmail(from_addr=user_id,
                                    to_addrs=person_email,
                                    msg= f"Subject:Happy Birthday!\n\n{named_content}")
    else:
        pass