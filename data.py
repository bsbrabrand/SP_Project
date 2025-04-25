class datastore:
    def __init__(self,time1,HR,reps):
        self.total_time=time1
        self.avg_HR=HR
        self.total_reps=reps
    def __str__(self):
        return f"Total time: {self.total_time} seconds\nAverage Heart rate: {self.avg_HR} bpm\nTotal reps: {self.total_reps} reps"



# test = datastore()
# test.avgHR=60
# print(test)

