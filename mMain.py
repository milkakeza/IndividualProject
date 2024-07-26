#!/usr/bin/python3
"""
1.This script provides a command-line interface for managing a Grade Book system with options to add students and courses,
2.register students for courses, calculate rankings, search for grades, and generate student transcripts.
3.It includes input validation to ensure correct data entry for students and courses, and allows users to save transcripts to files.
4.The script utilizes a menu-driven approach to facilitate user interaction with the GradeBook class.

"""
from Grrade_book import GradeBook
from datetime import datetime
import re
import time
import os




def print_menu():
    menu = [
        "1. Add Student",
        "2. Add Course",
        "3. Register Student for Course",
        "4. Calculate Ranking",
        "5. Search by Grade",
        "6. Generate Transcript",
        "7. Exit"
    ]
    
    print("\n" + "*" * 40)
    print(f"        MENU OPTIONS")
    print("*" * 40)

    for item in menu:
        print(f"{item:<36} ")
        
    
      

def main():
    grade_book = GradeBook()
    

    while True:
        print_menu()

        choice = input("\nEnter your choice: ")


        if choice == '1':
            while True:
                email = input("\nEnter student's email:")
                if not email:
                    print("Email is required!\n")
                elif grade_book.get_student_by_email(email):
                    print("Email already exists!\n")
                elif not email.endswith("@alustudent.com") or email.endswith("@gmail.com"):
                    print("Invalid Email Address!\n")
                else:
                    break
            
            while True:
                names = input("\nEnter student's names: ")
                if not names:
                    print("Names are required!\n")
                    continue
                if not re.match(r'^[a-zA-Z\s]+$', names):
                    print("Enter A Valid Name!\n")
                    continue
                break


        elif choice == '2':
            while True:
                name = input("Enter course name: ")
                if not name:
                    print("Course name is required!\n")
                    continue
                if not re.match(r'^[a-zA-Z\s]+$', name):
                    print("Enter A Valid Name of Course!\n")
                    continue
                courses_list = []
                with open("./data/courses.txt", "r") as courses:
                    for line in courses:
                        course_name, trimester, credits = line.strip().split(",")
                        courses_list.append(course_name)
                    if not name:
                        print("Course name is required!\n")
                    elif name in courses_list:
                        print("Course already exists!\n")
                    else:
                        break
            
            trimesters = ["1st", "2nd", "3rd"]
            while True:
                trimester = input("Enter trimester: ")
                if not trimester:
                    print("Trimester is required!\n")
                    continue
                
                else:
                    break
            while True:
                
                credits = (input("Enter course credits: "))
                if not credits:
                    print("Credits are required!\n")
                    continue
                elif re.match("^[0-9]*$", credits) == None:
                    print("Credits must be an integer and >0!\n")
                    continue
                else:
                    break
            grade_book.add_course(name, trimester, credits)

        elif choice == '3':
            while True:
                student_email = input("Enter student's email: ")
            
                if not student_email:
                    print("Email is required!\n")
                else:
                    student_emails = []
                    student_found = False
                    with open("./data/students.txt", "r") as file:
                        for line in file:
                            email, names, id = line.strip().split(",")
                            student_emails.append(email)
                            if student_email == email:
                                print(f"Student Found: ({names} ID: {id})\n")
                                student_found = True
                                break
            
                    if not student_found:
                        print("Oops :( , Student not found!\n")
                    else:
                        break
            
            while True:
                course_name_input = input("Enter course name: ")
                if not course_name_input:
                    print("Course name is required!\n")
                    continue
            
                course_found = False
                existing_courses = []
            
                with open("./data/courses.txt", "r") as file:
                    for line in file:
                        name, trimester, credits = line.strip().split(",")
                        existing_courses.append(name)
                        if course_name_input == name:
                            print(f"Course Found: {name} (Trimester: {trimester}, Credits: {credits})\n")
                            course_found = True
            
                if not course_found:
                    print("Oops :( , Course not found!\n")
                    print("Choose from already existing courses:")
                    for course in existing_courses:
                        print(f"{course}\n")
                    continue
            
                registered = False
                with open("./data/registered_courses.txt", "r") as file:
                    for line in file:
                        registered_email, registered_course_name, _ = line.strip().split(",")
                        if student_email == registered_email and course_name_input == registered_course_name:
                            print("You've registered for this course already\n")
                            registered = True
                            break
            
                if not registered:
                    break
        
            while True:
                score = input("Enter grade ( __/100): ")
                if not score:
                    print("Grade is required!\n")
                
                else:
                    try:
                        grade, highest_score = map(float, score.split('/'))
                        if grade > highest_score:
                            print("Invalid grade! The obtained score cannot be greater than the highest possible score.\n")
                        else:
                            calculated_grade = (grade / highest_score) * 4.0
                            print(f" Grade obtained: {calculated_grade:.2f}\n")
                            break
                    except ValueError:
                        print("Invalid grade format!\n")
                
            grade_book.register_student_for_course(student_email, course_name_input, calculated_grade)

        elif choice == '4':
            ranking = grade_book.calculate_ranking()
            num = 1
            print(f"\nRank:\n")
            for names, GPA in ranking:
                print(f"{num}.{names}: {GPA:.2f}\n")
                num += 1

        elif choice == '5':
            while True:
                course_name = input("Enter course name: ")
                if not course_name:
                    print("Course name is required!\n")
                    continue

                found = False
                existing_courses = []

                with open("./data/courses.txt", "r") as file:
                    for line in file:
                        name, trimester, credits = line.strip().split(",")
                        existing_courses.append(name)
                        if course_name == name:
                            print(f"Course name: {name} (Trimester: {trimester}, Credits: {credits})\n")
                            found = True
                            break

                    if not found:
                        print("Course not found!\n")
                        print("Choose from already existing courses:")
                        for course in existing_courses:
                            print(course)
                            continue

                if found:
                    break

            while True:
                small_grade = input("Enter minimum grade: ")
                if not small_grade:
                    print("Minimum grade is required!\n")
                else:
                    try:
                        small_grade = float(small_grade)
                        break
                    except ValueError:
                        raise ValueError("Grade is either a whole number or a decimal_point number!\n")
            
            while True:
                highest_grade = input("Enter maximum grade: ")
                if not highest_grade:
                    print("Maximum grade is required!\n")
                else:
                    try:
                        highest_grade = float(highest_grade)
                        break
                    except ValueError:
                        raise ValueError("Grade is either a whole number or a decimal_point number!\n")
            results = grade_book.search_by_grade(course_name, (small_grade, highest_grade))
            print("\nResults:")
            for names, grade in results:
                print(f"{names}: {grade}")

        elif choice == '6':
            while True:
                student_email = input("Enter student's email: ")
                if not student_email:
                    print("Email is required!\n")
                else:
                    student_emails = []
                    student_found = False
                    with open("./data/students.txt", "r") as file:
                        for line in file:
                            email, names, id = line.strip().split(",")
                            student_emails.append(email)
                            if student_email == email:
                                print(f"Student Found: ({names} ID: {id})\n")
                                student_found = True
                                break

                    if not student_found:
                        print("Student not found!\n")
                    else:
                        break

            transcript = grade_book.generate_transcript(student_email)
            if transcript:

                print(f" STUDENT TRANSCRIPT: \n")
                print(f"Student's Names: {transcript['names']}\n")
                print(f"Email: {transcript['email']}\n")
                print("Courses:\n")
            
                
                max_name_length = max(len(course) for course, _ in transcript['courses'])
                max_grade_length = max(len(f"{grade:.2f}") for _, grade in transcript['courses'])
            
                
                max_name_length = max(max_name_length, len("Name"))
                max_grade_length = max(max_grade_length, len("Grade"))
            
                print(f"{'Name':<{max_name_length}} | {'Grade':<{max_grade_length}}")
                print("-" * (max_name_length + max_grade_length + 3))
                
            
                
                for course, grade in transcript['courses']:
                    grade_str = f"{grade:.2f}"
                    print(f"{course:<{max_name_length}} | {grade_str:<{max_grade_length}}")
                    print("-"* (max_name_length + max_grade_length + 3))

            
        
                print(f"\nGPA: {transcript['GPA']:.2f}\n")
                print("*" * 53 + "\n")

                while True:
                    choice = input("Do you want to save the transcript to a file(yes or no)?\n")
                    if choice.lower() == 'yes':
                        with open("./data/students.txt", "r") as st:
                            for line in st:
                                email, names = line.strip().split(",")
                                if student_email == email:
                                    transcript['names'] = names
                                    break
                        with open(f"{transcript['names']}_transcript.txt", "w") as file:
                            file.write("="*53 + "\n")
                            file.write(f"{' '*20}STUDENT TRANSCRIPT{' '*20}\n")
                            file.write("="*53 + "\n\n")
                            file.write(f"Names: {transcript['names']}\n")
                            file.write(f"Email: {transcript['email']}\n")
                            file.write("\n")
                            file.write("-"*20 + " Courses " + "-"*20 + "\n")
                            file.write("\n")
                            file.write(f"{'Name':<{max_name_length}} | {'Grade':<{max_grade_length}}\n")
                            file.write("-" * (max_name_length + max_grade_length + 3))
                            file.write("\n")
                            for course, grade in transcript['courses']:
                                grade_str = f"{grade:.2f}"
                                file.write(f"{course:<{max_name_length}} | {grade_str:<{max_grade_length}}\n")
                                file.write("-"* (max_name_length + max_grade_length + 3))
                                file.write("\n")

                            file.write(f"\nGPA: {transcript['GPA']:.2f}\n")
                            file.write("=" * 53 + "\n")
                        print("\033[92mTranscript saved successfully!\033[0m")
                        break
                    elif choice.lower() == 'no':
                        break
                    else:
                        print("Invalid choice!\n")
            else:
                print("Student not found!")

        elif choice == '7':
            break

        else:
            print(" Oops :( , Invalid choice.\n")


    

if __name__ == "__main__":
    main()
