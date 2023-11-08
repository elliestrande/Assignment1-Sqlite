import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect('/Users/elliestrande/Desktop/database/408Assignment1/identifier.sqlite')
cursor = conn.cursor()

# import the students.csv file into the Students table
with open('/Users/elliestrande/Desktop/database/408Assignment1/students.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # iterate through the rows
    for row in csv_reader:
        cursor.execute("INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber')"
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                       (row['FirstName'], row['LastName'], row['GPA'], row['Major'], row['Address'], row['City'], row['State'], row['ZipCode'], row['MobilePhoneNumber']))

        # initialize isDeleted to - so that all Students are "existing" until made otherwise ('isDeleted' = 1)
        cursor.execute("UPDATE Student SET isDeleted = 0")

        # commit changes to the database
        conn.commit()

# close the database
conn.close()

# boolean to keep track of if user wants to continue
keep_going = True
while keep_going == True:
    # while keep_going == True:
    print('What option would you like to execute:')
    print('1) Display All Students and all of their attributes')
    print('2) Add new Students')
    print('3) Update Students')
    print('4) Delete Students by StudentId')
    print('5) Search/Display students by Major, GPA, City, State, and Advisor')
    print('6) Exit')

    while True:
        # take in users input between 1 and 6
        user_input = input("Enter a number between 1 and 6: ")

        # error handling to ensure the input is a number between 1 and 6
        try:
            x = float(user_input)
            if 1 <= x <= 6:
                break  # Exit the loop if a valid number is entered
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # if user_input = 1 display ALL students and all of their attributes
    if x == 1:
        conn = sqlite3.connect('/Users/elliestrande/Desktop/database/408Assignment1/identifier.sqlite')
        cursor = conn.cursor()

        # create SELECT statement to produce this result to standard output
        cursor.execute("SELECT * FROM Student")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        cursor.close()

    # if user_input = 2 add new students
    if x == 2:
        conn = sqlite3.connect('/Users/elliestrande/Desktop/database/408Assignment1/identifier.sqlite')
        cursor = conn.cursor()

        # user enters first and last names
        first_name = input('Enter First Name: ')
        last_name = input('Enter Last Name: ')

        # have user enter GPA and make sure it is a valid GPA
        while True:
            try:
                gpa = input('Enter GPA: ')
                gpa = float(gpa)
                if 0 <= gpa <= 4:
                    break
                else:
                    print("Invalid input. Please enter GPA between 0 and 4")
            except ValueError:
                print("Invalid input. Please enter a valid GPA between 0 and 4.")

        major = input('Enter Major: ')
        faculty_advisor = input('Enter Faculty Advisor: ')
        address = input('Enter Address: ')
        city = input('Enter City: ')

        # have the user input the students state and make sure it is a valid state
        while True:
            state = input('Enter State: ')

            valid_states = ["alabama", "alaska", "arizona", "arkansas", "california",
                            "colorado", "connecticut", "delaware", "florida", "georgia",
                            "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas",
                            "kentucky", "louisiana", "maine", "maryland", "massachusetts",
                            "michigan", "minnesota", "mississippi", "missouri", "montana",
                            "nebraska", "nevada", "new hampshire", "new jersey",
                            "new mexico", "new york", "north carolina", "north dakota",
                            "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island",
                            "south carolina", "south dakota", "tennessee", "texas", "utah",
                            "vermont", "virginia", "washington", "west virginia",
                            "wisconsin", "wyoming"]

            if state.lower() in valid_states:
                break
            else:
                print("Invalid input. Please enter a valid state.")

        # have the user input a zip code and make sure it is valid
        while True:
            zipcode = input('Enter a 5-digit Zip Code: ')
            if len(zipcode) == 5 and zipcode.isdigit():
                break
            else:
                print("Invalid input. Please enter a valid 5-digit zip code.")

        phone_number = input('Enter Mobile Phone Number: ')
        is_deleted = 0

        # insert the student into the database
        cursor.execute(
            "INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted')"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (first_name, last_name, gpa, major, faculty_advisor, address, city, state, zipcode, phone_number, is_deleted))
        conn.commit()
        conn.close()

    # if user_input = 3 update students
    if x == 3:
        conn = sqlite3.connect('/Users/elliestrande/Desktop/database/408Assignment1/identifier.sqlite')
        cursor = conn.cursor()

        print("Only the following fields can be updated: Major, Advisor, Mobile Phone Number")
        print("1) Major")
        print("2) Advisor")
        print("3) Mobile Phone Number")

        # obtain user input for what field will be updated
        while True:
            user_input1 = input("Which field would you like to update? (Enter a number 1-3)")

            try:
                x1 = float(user_input1)
                if 1 <= x1 <= 3:
                    break  # Exit the loop if a valid number is entered
                else:
                    print("Invalid input. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number between 1 and 3.")

        while True:
            # gets studentID that user wants to update and error handles to make sure it is a valid studentID in the database
            update_studentID = input("What is the studentID of the student you would like to update? ")
            try:
                student_id = int(update_studentID)
            except ValueError:
                print("Invalid input. Please enter a valid studentID: ")
                continue

            # Check if the studentID exists in the Student table
            cursor.execute("SELECT * FROM Student WHERE studentID = ?", (student_id,))
            if cursor.fetchone() is not None:
                break
            else:
                print(f"No student found with studentID {student_id} in the database.")

        # if 1 inputted update major
        if x1 == 1:
            new_major = input("Enter the major you would like to update this student to: ")
            cursor.execute("UPDATE Student SET Major = ?  WHERE StudentID == ?", (new_major, student_id))
            print("Major successfully updated!")

        # if 2 inputted update Advisor
        if x1 == 2:
            new_advisor = input("Enter the advisor you would like to update this student to: ")
            cursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentID == ?", (new_advisor, student_id))
            print("Advisor successfully updated!")

        # if 3 inputted update Mobile Phone Number
        if x1 == 3:
            new_phonenum = input("Enter the mobile phone number you would like to update this student to: ")
            cursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID == ?", (new_phonenum, student_id))
            print("Phone number successfully updated!")

        conn.commit()
        conn.close()

    # if user_input = 4 delete students by StudentID
    if x == 4:
        conn = sqlite3.connect('/Users/elliestrande/Desktop/database/408Assignment1/identifier.sqlite')
        cursor = conn.cursor()

        # gets the studentID that the user wants to delete and error handles to make sure it is a valid student id in the database
        while True:
            deleted_student = input('Enter the StudentID of the student you want to delete: ')
            try:
                deleted_student_id = int(deleted_student)
            except ValueError:
                print("Invalid input. Please enter a valid studentID: ")
                continue

            # Check if the studentID exists in the Student table
            cursor.execute("SELECT * FROM Student WHERE studentID = ?", (deleted_student_id,))
            if cursor.fetchone() is not None:
                break
            else:
                print(f"No student found with studentID {deleted_student_id} in the database.")

        # perform a soft delete
        cursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentID == ?", (1, deleted_student_id))
        conn.commit()
        conn.close()

        print('Successfully deleted!')
        print('')

    # if user_input = 5 search/display students by Major, GPA, City, State, and Advisor
    if x == 5:
        conn = sqlite3.connect('/Users/elliestrande/Desktop/database/408Assignment1/identifier.sqlite')
        cursor = conn.cursor()

        # ask users what they want to search students by
        print("Search students by:")
        print("1) Major")
        print("2) GPA")
        print("3) City")
        print("4) State")
        print("5) Advisor")

        # recieve user input and make sure it is a valid number between 1 and 5
        while True:
            user_input2 = input('Enter your selection as a number 1-5: ')
            try:
                x2 = int(user_input2)
                if 1 <= x2 <= 5:
                    break  # Exit the loop if a valid number is entered
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # modify the query base depending on the users input
        # search by major
        # modify the query base depending on the users input
        # search by major
        if x2 == 1:
            # get all unique 'Major' values
            cursor.execute("SELECT DISTINCT Major FROM Student")
            unique_majors = [row[0] for row in cursor.fetchall()]

            while True:
                search_value = input("Enter the Major (Case Sensitive): ")
                if search_value in unique_majors:
                    break
                else:
                    print('Major not found. Please enter a valid Major.')

            # selects students with inputted major
            cursor.execute("SELECT * FROM Student WHERE Major = ?", (search_value,))
            rows = cursor.fetchall()

            # print the results
            for row in rows:
                print(row)

        # search by GPA
        elif x2 == 2:  # Search by GPA
            cursor.execute("SELECT DISTINCT GPA FROM Student")
            unique_GPAs = [float(row[0]) for row in cursor.fetchall()]

            # ensures GPA is a float and is in the database
            while True:
                try:
                    search_value = input("Enter the GPA: ").strip()
                    search_value = float(search_value)

                    if search_value in unique_GPAs:
                        break
                    else:
                        print('GPA not found. Please enter a valid GPA.')
                except ValueError:
                    print('Invalid input. Please enter a valid GPA.')

            # selects students with inputted GPA
            cursor.execute("SELECT * FROM Student WHERE GPA = ?", (search_value,))
            rows = cursor.fetchall()

            # print the results
            for row in rows:
                print(row)

        # search by City
        elif x2 == 3:
            cursor.execute("SELECT DISTINCT City FROM Student")
            unique_cities = [row[0] for row in cursor.fetchall()]

            while True:
                search_value = input("Enter the City (Case Sensitive): ")
                if search_value in unique_cities:
                    break
                else:
                    print('City not found. Please enter a valid City.')

            cursor.execute("SELECT * FROM Student WHERE City = ?", (search_value,))
            rows = cursor.fetchall()

            # print the results
            for row in rows:
                print(row)

        # search by State
        elif x2 == 4:
            cursor.execute("SELECT DISTINCT State FROM Student")
            unique_states = [row[0] for row in cursor.fetchall()]

            while True:
                search_value = input("Enter the State (Case Sensitive): ")
                if search_value in unique_states:
                    break
                else:
                    print('State not found. Please enter a valid State.')

            cursor.execute("SELECT * FROM Student WHERE State = ?", (search_value,))
            rows = cursor.fetchall()

            # print the results
            for row in rows:
                print(row)

        # search by Advisor
        elif x2 == 5:
            # get unique advisors from FacultyAdvisor row
            cursor.execute("SELECT DISTINCT FacultyAdvisor FROM Student")
            unique_advisors = [row[0] for row in cursor.fetchall()]

            while True:
                # search to see if value is an advisor in the database
                search_value = input("Enter the Advisor (Case Sensitive): ")
                if search_value in unique_advisors:
                    break
                else:
                    print('Advisor not found. Please enter a valid Advisor.')

            cursor.execute("SELECT * FROM Student WHERE FacultyAdvisor = ?", (search_value,))
            rows = cursor.fetchall()

            # print the results
            for row in rows:
                print(row)

        else:
            print("Invalid input. Please enter a number between 1 and 5.")

        conn.close()

    # if user input is 6, exits the while loop and ends the process
    if x == 6:
        keep_going = False


