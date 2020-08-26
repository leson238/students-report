class Test:
    """Test data models"""
    TEST_ID = set()
    TESTS_TABLE = []

    def __init__(self, test_id):
        self._set_test_id(test_id)
        self._set_test_information()

    def _set_test_id(self, test_id):
        if test_id not in Test.TEST_ID:
            Test.TEST_ID.add(test_id)
        self.test_id = test_id

    def _set_test_information(self):
        if hasattr(self, 'test_id'):
            for row in Test.TESTS_TABLE:
                if row['id'] == self.test_id:
                    self.course_id = row['course_id']
                    self.weight = int(row['weight'])
                    break

    def __str__(self):
        return f"Test_id: {self.test_id}, course_id: {self.course_id}, weight: {self.weight}"
