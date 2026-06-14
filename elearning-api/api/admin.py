from django.contrib import admin
from .models import CourseName, FullCourse,Videolist,BookCategory,Book,Notification

admin.site.register(CourseName)
admin.site.register(FullCourse)
admin.site.register(Videolist)
admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(Notification)
