from django.urls import path
from .views import FullCourseDetail, Register, Login, CourseCategory, CourseCategoryDetail,FullCourselist,Profile,VideoListView,VideoLisetDatail,CategoryBook,CategoryBookDetail,BookLibrary,BookLibraryDetail,NotificationApp
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('courses-category/', CourseCategory.as_view()),
    path('courses-category/<int:pk>/', CourseCategoryDetail.as_view()),
    path('courses/', FullCourselist.as_view()),
    path('courses/<int:pk>/', FullCourseDetail.as_view()),
    path('profile/',Profile.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('courselist/',VideoListView.as_view()),
    path('courselist/<int:pk>/',VideoLisetDatail.as_view()),
    path('book/category/', CategoryBook.as_view()),
    path('book/category/<int:pk>/', CategoryBookDetail.as_view()),
    path('book/',BookLibrary.as_view()),
    path('book/<int:pk>/', BookLibraryDetail.as_view()),
    path('notification/',NotificationApp.as_view()),

]
