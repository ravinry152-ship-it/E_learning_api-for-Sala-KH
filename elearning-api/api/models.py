from django.db import models
from django.conf import Settings
from django.contrib.auth.models import User
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


class Quiz(models.Model):
    lesson = models.ForeignKey(Videolist, on_delete=models.CASCADE, related_name="quizzes", verbose_name="ស្ថិតក្នុងមេរៀនណា")
    title = models.CharField(max_length=255, verbose_name="ចំណងជើងការធ្វើតេស្ត (ឧ. តេស្តសមត្ថភាពមេរៀនទី១)")
    duration_minutes = models.IntegerField(default=15, verbose_name="រយៈពេលធ្វើតេស្ត (នាទី)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ({self.lesson.title})"

    class Meta:
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="ស្ថិតក្នុងកម្រងសំណួរណា")
    question_text = models.TextField(verbose_name="ខ្លឹមសារប្រធានសំណួរ")
    order = models.PositiveIntegerField(default=1, verbose_name="លំដាប់សំណួរ (ទី១, ទី២...)")

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"

    class Meta:
        ordering = ['order']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices", verbose_name="ជម្រើសរបស់សំណួរណា")
    prefix = models.CharField(max_length=2, verbose_name="តួអក្សរមុខ (A, B, C, D)")
    choice_text = models.CharField(max_length=255, verbose_name="ខ្លឹមសារចម្លើយ")
    is_correct = models.BooleanField(default=False, verbose_name="ជាចម្លើយត្រឹមត្រូវពិតប្រាកដ")

    def __str__(self):
        return f"{self.prefix}. {self.choice_text} ({'ត្រូវ' if self.is_correct else 'ខុស'})"


class QuizSubmission(models.Model):
    user = models.ForeignKey(Settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_submissions", verbose_name="សិស្សដែលបានធ្វើ")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="submissions", verbose_name="វិញ្ញាសាដែលបានធ្វើ")
    score = models.IntegerField(verbose_name="ពិន្ទុដែលទទួលបាន (ពេញ ១០០)")
    total_questions = models.IntegerField(verbose_name="ចំនួនសំណួរសរុប")
    correct_answers = models.IntegerField(verbose_name="ចំនួនឆ្លើយត្រូវ")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="កាលបរិច្ឆេទប្រឡង")

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score} ពិន្ទុ)"






