from tkinter import *
import sqlite3


root = Tk()
root.title('Student Analysis')
root.geometry('800x600') 


conn=sqlite3.connect('student_data.db')

cursor=conn.cursor()
# cursor.execute('''CREATE TABLE student(
#     Student_name text,
#     Course_name text,
#     Course_score text
#     )''')

#creating a list to hold all the score of the students
student_score=[]
def add_students():
    conn=sqlite3.connect('student_data.db') #connecting to the database to access it
    cursor= conn.cursor()
    cursor.execute('INSERT INTO student VALUES(:student_name, :course_name, :course_scores)',#adding values to the database
                {
                    'student_name':student_name.get(),
                    'course_name':course_name.get(),
                    'course_scores':course_scores.get()
                })
    conn.commit()
    print('Student added')
    student_name.delete(0, END)
    course_name.delete(0, END)
    course_scores.delete(0, END)
    conn.close()


#Function to get the average of the total scores
def calc_avg():
    conn=sqlite3.connect('student_data.db')
    cursor= conn.cursor()
    query="SELECT course_score FROM student"
    cursor.execute(query)
    scores=cursor.fetchall()
    
    #querying data from the database(its a tuple) to get all the scores and put them in a list
    for score in scores:
        values=score[0]
        student_score.append(values)
    
    #converting each value in the list to decimal
    new_scores= list(map(float, student_score))
    
    avg=sum(new_scores)/len(new_scores)
    avg_resut=Label(root, text=f"Total Students average is {avg}")
    avg_resut.grid(row=7, column=0)
    conn.close()





def position():
    
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    
    # Use a single query to select and sort the scores
    query = "SELECT student_name, course_score FROM student ORDER BY course_score DESC"
    
    cursor.execute(query)
    
    # Fetch all the results, which are already sorted
    sorted_students = cursor.fetchall()
    
    
    my_listbox = Listbox(root, font=font_style)
    my_listbox.grid(row=7, column=2)
    
    
    if sorted_students:
        print("Students sorted by score (highest to lowest):")
        x=0
        
        #querying to get each of thm names and results with their position
        for name, score in sorted_students:
            x += 1
            my_listbox.insert(END, f'{x}. {name}: {score}')
    else:
        print("No student data found.")
    
    # Close the database connection
    conn.close()


save_grades=[]
total_student=[]
secure_result=[]
def grade():
    conn=sqlite3.connect('student_data.db')
    cursor= conn.cursor()
    
    #getting data from the database
    query="SELECT course_score FROM student"
    cursor.execute(query)
    scores=cursor.fetchall()
    query2="SELECT student_name FROM student"
    cursor.execute(query2)
    students=cursor.fetchall()
    
    #adding data to a list
    for student in students:
        people=student[0]
        total_student.append(people)
        
    result_listbox=Listbox(root,font=font_style)
    result_listbox.grid(row=7, column=1)
    
    for score in scores:
        values=score[0]
        save_grades.append(values)
    
    record=list(map(float, save_grades))
    
    for grades in record:
        if grades >=75 :
            performance='A'
        elif grades>=65 and grades < 75:
            performance= 'B'
        elif grades>=50 and grades <65 :
            performance= 'C'
        elif grades >=45 and grades < 50 :
            performance= 'D'
        elif grades >=40 and grades < 45 :
            performance= 'E'
        else:
            performance= 'F'
        secure_result.append(performance)
    
    for student,result in zip(total_student,secure_result):
        result_listbox.insert(END, f'{student}: {result}')

























'''Styling'''




font_style = ('Helvetica', 12)
header_font = ('Helvetica', 14, 'bold')


input_frame = Frame(root, bg="#f9f6f6", padx=20, pady=20)
input_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

student_name_lbl = Label(input_frame, text='Student Name', font=font_style)
student_name_lbl.grid(row=0, column=0, sticky=W, padx=5, pady=5)
student_name = Entry(input_frame, width=35, borderwidth=2, relief='groove', font=font_style)
student_name.grid(row=1, column=0, padx=5, pady=5)

course_name_lbl = Label(input_frame, text='Course Name', font=font_style)
course_name_lbl.grid(row=0, column=1, sticky=W, padx=5, pady=5)
course_name = Entry(input_frame, width=20, borderwidth=2, relief='groove', font=font_style)
course_name.grid(row=1, column=1, padx=5, pady=5)

course_scores_lbl = Label(input_frame, text='Course Score (100)', font=font_style)
course_scores_lbl.grid(row=0, column=2, sticky=W, padx=5, pady=5)
course_scores = Entry(input_frame, width=10, borderwidth=2, relief='groove', font=font_style)
course_scores.grid(row=1, column=2, padx=5, pady=5)


add_student = Button(root, text='Add to record', width=50, font=font_style, bg='green', fg='white', cursor='hand2', command=add_students)
add_student.grid(row=2, column=0, columnspan=3, pady=10, padx=10)


separator1 = Frame(root, height=2, bd=1, relief='sunken')
separator1.grid(row=3, column=0, columnspan=3, sticky='ew', padx=10, pady=5)

description = Label(root, text="Analyze all students", font=header_font, pady=10)
description.grid(row=4, column=0, columnspan=3)

separator2 = Frame(root, height=2, bd=1, relief='sunken')
separator2.grid(row=5, column=0, columnspan=3, sticky='ew', padx=10, pady=5)


average_btn = Button(root, text="Get students average", font=font_style, bg='blue', fg='white', relief='raised', cursor='hand2', command=calc_avg)
average_btn.grid(row=6, column=0, pady=10, padx=5, sticky='ew')

grade_btn = Button(root, text="Get students grades", font=font_style, bg='blue', fg='white', relief='raised', cursor='hand2', command=grade)
grade_btn.grid(row=6, column=1, pady=10, padx=5, sticky='ew')

position_btn = Button(root, text="Get students position", font=font_style, bg="#0641B7", fg='white', relief='raised', cursor='hand2', command=position)
position_btn.grid(row=6, column=2, pady=10, padx=5, sticky='ew')

root.mainloop()