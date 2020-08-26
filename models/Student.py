"""Import"""
from .Test import Test
from .Mark import Mark


class Course:
    """Courses data models"""
    COURSES_TABLE = []

    def __init__(self, course_id):
        self.course_id = str(course_id)
        self._set_course_information()
        self.weights = {}
        self._add_tests()

    def _set_course_information(self):
        for row in Course.COURSES_TABLE:
            if row['id'] == self.course_id:
                self.name = row['name']
                self.teacher = row['teacher']

    def _add_tests(self):
        self.tests = []
        for test_id in Test.TEST_ID:
            if Test(test_id).course_id == self.course_id:
                self.tests.append(Test(test_id))
        self._weight_calibrate()

    def _weight_sum(self):
        """
        Return total weight of course's tests
        """
        s = sum([test.weight for test in self.tests])
        if s != 100:
            raise Exception(
                f"Sum of test weights in {self.name} is not equal to 100")
        return s

    def _weight_calibrate(self):
        """Calibrate test's weight to have the sum of 100"""
        self._weight_sum()
        for test in self.tests:
            self.weights[test.test_id] = round(
                test.weight / 100, 2)

    def __str__(self):
        return f"{self.weights}"


class Student:
    """Student data models"""
    STUDENT_ID = set()
    STUDENTS_TABLE = []

    def __init__(self, student_id, name):
        self._set_student_id(student_id)
        self.name = name
        self._marks = []
        self.enrolled_courses = {}
        self.course_teacher = {}
        self.course_id = {}
        self._add_marks()
        self._add_course()

    def _set_student_id(self, student_id):
        if student_id not in Student.STUDENT_ID:
            self.student_id = student_id
            Student.STUDENT_ID.add(student_id)
        else:
            raise ValueError('Student ID is not unique')

    def _add_marks(self):
        """add mark to specific student"""
        marks = []
        for row in Mark.MARKS_TABLE:
            marks.append(
                Mark(row['test_id'], row['student_id'], int(row['mark'])))
        for mark in marks:
            if mark.student_id == self.student_id:
                self._marks.append(mark)

    def _add_course(self):
        test_list = set()
        should_take = {}
        for mark in self._marks:
            if mark.test_id not in test_list:
                test_list.add(mark.test_id)
                test = Test(mark.test_id)
                course = Course(test.course_id)
                should_take[course.name] = len(course.weights)
                weighted_mark = mark.mark * \
                    course.weights[test.test_id]
                if course.name not in self.enrolled_courses:
                    self.enrolled_courses[course.name] = [weighted_mark]
                    self.course_teacher[course.name] = course.teacher
                    self.course_id[int(test.course_id)] = course.name
                else:
                    self.enrolled_courses[course.name].append(
                        weighted_mark)
        for course_name in self.enrolled_courses:
            test_taken = len(self.enrolled_courses[course_name])
            if test_taken != should_take[course_name]:
                raise Exception(
                    f"Student {self.name} did not taken enough test in {course_name}")

    def get_course_average(self, course_name):
        """return average for each course"""
        course_avg = sum(self.enrolled_courses[course_name])
        if course_avg > 100:
            course_avg = 100
        return course_avg

    def get_total_average(self):
        """Return total average of a student"""
        if len(self.enrolled_courses) > 0:
            total = 0
            for course in self.enrolled_courses:
                total += self.get_course_average(course)
            total_avg = round(total / len(self.enrolled_courses), 2)
            if total_avg > 100:
                total_avg = 100
            return total_avg
        return 0

    def __str__(self):
        student = [
            f"""\
Student Id: {self.student_id}, name: {self.name}
Total Average:        {round(self.get_total_average(),2)}% \n"""]
        for course_id in sorted(self.course_id):
            course_name = self.course_id[course_id]
            student.append(
                f"""
    Course: {course_name}, Teacher: {self.course_teacher[course_name]}
    Final Grade:      {round(self.get_course_average(course_name),2)}% \n
""")
        return "".join(student)
