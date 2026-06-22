from django.contrib import admin
from .models import (
    CourseName, FullCourse,
    Videolist,BookCategory,
    Book,Notification,
    Question,
    Quiz,
    Choice,
    QuizSubmission,
    MainCourse
)

admin.site.register(CourseName)
admin.site.register(FullCourse)
admin.site.register(Videolist)
admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(Notification)
admin.site.register(Quiz),
admin.site.register(Question),
admin.site.register(Choice),
admin.site.register(QuizSubmission),
admin.site.register(MainCourse)
