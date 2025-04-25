import time

class datastore:
    def __init__(self,time1,HR,reps,ID):
        self.total_time=time1
        self.avg_HR=HR
        self.total_reps=reps
        self.ID=ID
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
        self.endtime = formatted_time
    def __str__(self):
        return f"{self.ID}\nFinished at {self.endtime}\nTotal time: {self.total_time:.2f} seconds\nAverage Heart rate: {self.avg_HR:.2f} bpm\nTotal reps: {self.total_reps} reps"


