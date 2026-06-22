from rest_framework import serializers
from .models import (
    CourseName, FullCourse,Videolist, 
    BookCategory, Book,Notification,
    Question,
    Quiz,
    Choice,
    QuizSubmission,
    MainCourse,
)

class MainCourseSerializer(serializers.ModelSerializer) :
    class Meta :
        model = MainCourse
        fields = "__all__"

class VideoListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='course.course_name.course_name', read_only=True)
    course_title = serializers.CharField(source='course.course_description', read_only=True)

    class Meta:
        model = Videolist
        fields = ['id', 'category', 'course_title', 'title', 'video_url', 'duration']

class FullCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullCourse
        fields = ['id', 'course_name', 'course_description', 'image']

class CourseNameSerializer(serializers.ModelSerializer):
    full_courses = FullCourseSerializer(many=True, read_only=True)
    class Meta:
        model = CourseName
        fields = ['id', 'course_name', 'full_courses']


class BookSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Book
        fields = "__all__"


class  BookCategorySerializer(serializers.ModelSerializer) :
    books = BookSerializer(many=True, read_only=True)
    class Meta :
        model = BookCategory
        fields =['id', 'book_category_name', 'books']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Notification
        fields = "__all__"
        

class QuizSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Quiz
        fields = ['id',' lesson', 'title','duration_minutes','created_at']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'prefix', 'choice_text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'order', 'choices']

class QuizSubmissionSerializer(serializers.ModelSerializer) :
    quiz_title = QuizSerializer(read_only=True)
    class Meta :
        model = QuizSubmission
        fields = '__all__'



