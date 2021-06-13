import sys
from crontab import CronTab

myCron = CronTab(user='pi')


class CronJob(object):

    def __init__(self, hr, min) -> None:
        self.hr = hr
        self.min = min

    def make(self):
        job = myCron.new(
            command='python3 /home/pi/Desktop/tengku/src/soundrecord.py', comment="Tengku")
        job.setall(self.min, self.hr, '*', '*', '*')
        print("New Cron Job Created")
        myCron.write()

    def update(self):
        for job in myCron:
            if job.comment == "Tengku":
                job.setall(self.min, self.hr, '*', '*', '*')
                print("Cront Updated")
                myCron.write()

    def remove(self):
        for job in myCron:
            if job.comment == "Tengku":
                job.setall(self.min, self.hr, '*', '*', '*')
                myCron.remove(job)
                print("Cront Deleted")
                myCron.write()

    def show(self):
        for job in myCron:
            print(job)
