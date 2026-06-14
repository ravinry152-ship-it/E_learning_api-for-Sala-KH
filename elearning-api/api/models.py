from django.db import models

class CourseName(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)
    def __str__(self):
        return self.course_name

class FullCourse(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.ForeignKey(CourseName, on_delete=models.CASCADE,related_name='full_courses')
    course_description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    def __str__(self):
        return self.course_description
    
class Videolist(models.Model):
    id= models.AutoField(primary_key=True)
    course = models.ForeignKey(FullCourse, on_delete=models.CASCADE, related_name='videos')    
    title = models.CharField(max_length=250, null=True, blank=True) #ចំណងជេីងCourse
    video_url = models.URLField(max_length=400, null=True, blank=True) 
    duration = models.CharField(max_length=50, blank=True, null=True) #នាទីin video

    def __str__(self):
        return f"{self.course.course_description} - {self.title}"
    
class BookCategory(models.Model) :
    id = models.AutoField(primary_key=True)
    book_category_name = models.CharField(max_length=200)
    def __str__(self):
       return self.book_category_name

class Book(models.Model):
    id= models.AutoField(primary_key=True)
    title= models.CharField(max_length=200)
    book_category_name = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='books')
    image = models.ImageField(upload_to='book_images/')
    book_pdf = models.FileField(upload_to='books/pdfs/')
    def __str__(self):
        return self.title
    
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title= models.CharField(max_length=100)
    description = models.TextField()






