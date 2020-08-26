import time
import os

from tkinter import filedialog, Tk, StringVar
from tkinter import Entry, Label, Button, Listbox, messagebox
from tkinter import END

from models.utilities import read_file, write_file
from models.Mark import Mark
from models.Test import Test
from models.Student import Course, Student

main_win = Tk()
main_win.title("Report Application")
main_win.sourceFolder = ''
currdir = os.getcwd()

# Place GUI in center of the screen for better UX
windowWidth = main_win.winfo_reqwidth()
windowHeight = main_win.winfo_reqheight()

positionRight = int(main_win.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(main_win.winfo_screenheight() / 2 - windowHeight / 2)

main_win.geometry("+{}+{}".format(positionRight, positionDown))


class UserInput:
    INPUT_PATH = ""
    OUTPUT_PATH = ""

    def __init__(self, main_win):
        Label(main_win, text='Input Folder').grid(row=0, sticky='W')
        self.input_value = StringVar()
        self.input_path = Entry(main_win, textvariable=self.input_value)
        self.input_path.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        self.b_input = Button(main_win, text="Browse...", command=self.chooseInput)
        self.b_input.grid(row=0, column=3, padx=5, pady=5)

        Label(main_win, text='Output Folder').grid(row=1, sticky='W')
        self.output_value = StringVar()
        self.output_path = Entry(main_win, textvariable=self.output_value)
        self.output_path.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.b_output = Button(main_win, text="Browse...", command=self.chooseOutput)
        self.b_output.grid(row=1, column=3, padx=5, pady=5)

    def chooseInput(self):
        UserInput.INPUT_PATH = filedialog.askdirectory(parent=main_win, initialdir=currdir, title='Please select a directory')
        self.input_path.insert(END, UserInput.INPUT_PATH)

    def chooseOutput(self):
        UserInput.OUTPUT_PATH = filedialog.askdirectory(parent=main_win, initialdir=currdir, title='Please select a directory')
        self.output_path.insert(END, UserInput.OUTPUT_PATH)


def setup_models():
    """Setup models by filling data and initialize start conditions"""

    Mark.MARKS_TABLE = read_file(UserInput.INPUT_PATH, "marks")

    Test.TESTS_TABLE = read_file(UserInput.INPUT_PATH, "tests")
    # initialize test_id
    for record in Test.TESTS_TABLE:
        Test(record['id'])

    Course.COURSES_TABLE = read_file(UserInput.INPUT_PATH, "courses")
    Student.STUDENTS_TABLE = read_file(UserInput.INPUT_PATH, "students")


def create_report():
    """Create report and logging error"""
    try:
        setup_models()
        STUDENTS = []
        for record in Student.STUDENTS_TABLE:
            STUDENTS.append(Student(record['id'], record['name']))
        DATA = ''.join(list(map(str, STUDENTS)))
        write_file(UserInput.OUTPUT_PATH, data=DATA)

        should_open = messagebox.askyesno(
            'Show Report File', 'Do you want to open Reports.txt? ')
        if should_open:
            os.system(f'start "" {UserInput.OUTPUT_PATH}\\reports.txt')
    except ValueError as error:
        from datetime import datetime
        time = datetime.now().strftime("%H:%M:%S")
        messagebox.showerror("Corrupted input", "Something is wrong with your data. See logs.txt for more details")
        with open("logs.txt", "w+") as f:
            print(f"{time} - {error}", file=f)


if __name__ == "__main__":
    browse_button = UserInput(main_win)
    b_create = Button(main_win, text='Create Reports.txt', command=create_report)
    b_create.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='NESW')
    main_win.mainloop()
