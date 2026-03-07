class StudentsMarks :
    def __init__(self,mark):
        self.mark = mark
    def last_three_avg(self):
        try:
            if len(self.mark)<3:
                raise Exception ("Not enough marks to calculate average")
            last_three=self.mark[-3:]
            avg = sum(last_three)/3
            print("avg of last three marks is", avg)        
        
        except Exception as e:
            print(e)

marks=[50,60,70,80,90]
student=StudentsMarks(marks)
student.last_three_avg()
         
