from rest_framework import serializers
from .models import CourseName, FullCourse,Videolist, BookCategory, Book,Notification


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
        fields = "__all__"



