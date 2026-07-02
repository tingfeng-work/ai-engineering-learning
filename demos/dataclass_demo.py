from dataclasses import dataclass


@dataclass()
class Student:
    name: str
    age: int
    school: str = "Waseda University"
    email: str | None = None


student1 = Student("李廷风", 25)
student2 = Student("小明", 18, "UESTC", "12345@.com")

print(student1)
print(student2)

print(f"name:{student1.name}", f"school:{student1.school}", f"email:{student1.email}")

student3 = Student("李廷风", 25)
print(student1 == student3)

print(Student.__init__)
print(Student.__repr__)

print(str(student1))
print(repr(student1))
