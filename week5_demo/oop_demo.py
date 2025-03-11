from typing import List

class Student:
    def __init__(self, n):
        self.name = n
        self.age = 20
    
    def getName(self):
        return self.name
    
    def setFullName(self, new_name):
        self.name = new_name

class Classroom:
    def __init__(self, title:str):
        self.title:str = title
        self.lst_students:List[Student] = []
        
    def addStudent(self, new_student:Student):
        ## Prevent to add new student if that person is already enrolled
        if isinstance(new_student, Student):
            for student in self.lst_students:
                if student == new_student:
                    return "This student is already enrolled"
            self.lst_students.append(new_student)
        else:
            print("YOu must be student to enroll")
        
    def listAllStudents(self):
        return self.lst_students
    
    def removeStudents(self):
        pass
    
s1 = Student("Sat")
s2 = Student("A Thet")

## Computer Science Class Object - create
cs = Classroom("Computer Science")

## Add student s1 s2
cs.addStudent(s1)
cs.addStudent(s2)
print(cs.listAllStudents())

## s2 twice - error msg?
cs.addStudent("Thet")
