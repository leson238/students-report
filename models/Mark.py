class Mark:
    """Mark data models"""
    MARKS_TABLE = []

    def __init__(self, test_id, student_id, mark):
        self.test_id = test_id
        self.student_id = student_id
        self._set_mark(mark)

    def _set_mark(self, mark):
        if mark < 0:
            self.mark = 0
        elif mark > 100:
            self.mark = 100
        else:
            self.mark = mark

    def __str__(self):
        return f"Test ID: {self.test_id}, Student ID: {self.student_id}, Mark: {self.mark}"
