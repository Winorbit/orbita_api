from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Course, Lesson

class CoursesAndLessonsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        test_course = Course.objects.create(id=1, 
                                            title="Test title", 
                                            description="Test description",
                                            content="Test course content",)

        test_lesson = Lesson.objects.create(title="Test Lesson", 
                                            description="Test description",
                                            content="Test lesson content",
                                            cours = test_course)
   
    def test_courses(self):
        response = self.client.get("/courses")
        self.assertEqual(response.status_code, 301)

        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/courses/00000000-0000-0000-0000-000000000001/")
        self.assertEqual(response.status_code, 200)
    
 
    def test_lessons(self):
        response = self.client.get("/lessons")
        self.assertEqual(response.status_code, 301)

        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, 200)
