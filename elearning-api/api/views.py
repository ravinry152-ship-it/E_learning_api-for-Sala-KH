from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CourseName, FullCourse, BookCategory, Book,Videolist, Notification
from django.contrib.auth.models import User
from .serializer import CourseNameSerializer, FullCourseSerializer, VideoListSerializer,BookCategorySerializer,BookSerializer,NotificationSerializer
class Register(APIView) :
    permission_classes = [AllowAny] 
    authentication_classes = []
    def post(self , request , format =None) :
        try :
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password or not username :
                return Response({
                    'error': "Username, email, and password are required"
                }, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({'error': 'គណនីនេះត្រូវបានចុះឈ្មោះរួចហេីយ'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'គណនីនេះធ្លាប់បានចុះឈ្មោះរួចហេីយ'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, email=email, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#====================================Login_api======================================

class Login(APIView) :
    permission_classes = [AllowAny,] 
    authentication_classes = []
    def post(self , request , format=None) :
        email = request.data.get('email')
        password = request.data.get('password')
        
        # កែប្រែលក្ខខណ្ឌឆែកត្រឹមតែ email និង password
        if not email or not password :
            return Response({
                'error': "សូមបញ្ចូល Email និងលេខសម្ងាត់ឱ្យបានត្រឹមត្រូវ"   
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try :
            user_obj = User.objects.get(email=email)
            username = user_obj.username 
        except User.DoesNotExist :
            return Response({
                'error': "មិនមានគណនីប្រើប្រាស់អ៊ីម៉ែលនេះទេ"
            }, status=status.HTTP_404_NOT_FOUND)
            
        if user_obj is not None :
            if user_obj.check_password(password):
                refresh = RefreshToken.for_user(user_obj)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': username
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': "ពាក្យសម្ងាត់មិនត្រឹមត្រូវទេ"
                }, status=status.HTTP_400_BAD_REQUEST)
            
class CourseCategory(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        courses = CourseName.objects.prefetch_related('full_courses').all()
        serializer = CourseNameSerializer(courses, many=True)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = CourseNameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'course': serializer.data}, status=status.HTTP_201_CREATED)
        print(serializer.errors,{"error": "Invalid data"})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class CourseCategoryDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk) :
        try :
            return CourseName.objects.get(pk=pk)
        except CourseName.DoesNotExist :
            return None
    def get(self , request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseNameSerializer(course)
        return Response({'course': serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        course = self.get_object(pk)
        if course is None :
            return Response({'error': 'course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseNameSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'course': serializer.data}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk) :
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class FullCourselist(APIView) :
    permission_classes = [IsAuthenticated]
    def get(self, request):
        category_id = request.query_params.get('category_id')
        
        if category_id:
            full_courses = FullCourse.objects.filter(category_id=category_id)
        else:
            full_courses = FullCourse.objects.select_related('course_name').all()
            
        serializer = FullCourseSerializer(full_courses, many=True)
        return Response({'full_courses': serializer.data}, status=status.HTTP_200_OK)
    def post(self, request, format= None):
        serializer= FullCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'full_course': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class FullCourseDetail(APIView) :
    permission_classes = [IsAuthenticated]
    def get_object(self, pk) :
        try :
            return FullCourse.objects.get(pk=pk)
        except FullCourse.DoesNotExist :
            return None
        
    def get(self, request, pk) :
        full_course= self.get_object(pk)
        if full_course is None:
            return Response({'error': 'Full course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FullCourseSerializer(full_course)
        return Response({'full_course': serializer.data}, status=status.HTTP_200_OK)
    
    def put(self ,request, pk) :
        full_course= self.get_object(pk)
        if full_course is None:
            return Response({'error': 'Full course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FullCourseSerializer(full_course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'full_course': serializer.data}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk) :
        full_course= self.get_object(pk)
        if full_course is None:
            return Response({'error': 'Full course not found'}, status=status.HTTP_404_NOT_FOUND)
        full_course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#===============profile user======================
class Profile(APIView):
   permission_classes=[IsAuthenticated]
   def get(self, request, *args, **kwargs):
        user = request.user  
        return Response({
            'username': user.username,
            'email': user.email
        })
   
#=================course list========================
class VideoListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Videolist.objects.all()

        # 1. Filter តាម ID របស់ FullCourse (Ex: Python Full Course ID = 1)
        course_id = request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # 2. Filter តាមឈ្មោះប្រភេទធំ (Ex: course_name = Programming ឬ Design)
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(course__course_name__course_name__iexact=category)

        serializer = VideoListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request) :
        serializer = VideoListSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response({'full_course': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#=======================put and delete  videolist====================================
class VideoLisetDatail(APIView):
     permission_classes=[IsAuthenticated]
     def get_object(self, pk) :
        try :
            return Videolist.objects.get(pk=pk)
        except Videolist.DoesNotExist :
            return None
        
     def get(self, request, pk) :
         videolist= self.get_object(pk)
         if videolist is None :
            return Response({'error': 'Full course not found'}, status=status.HTTP_404_NOT_FOUND)
         serializer= VideoListSerializer(videolist)
         return Response({'full_course': serializer.data}, status=status.HTTP_200_OK)
     
     def put(self, request, pk) :
         videolist= self.get_object(pk)
         if videolist is None:
            return Response({'error': 'video list not found'}, status=status.HTTP_404_NOT_FOUND)
         serializer = FullCourseSerializer(videolist, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response({'videolist': serializer.data}, status=status.HTTP_200_OK)
         print(serializer.errors)
         return Response({'error': 'videolist not found'}, status=status.HTTP_404_NOT_FOUND)
     
     def delete(self, request, pk) :
        videolist= self.get_object(pk)
        if videolist is None:
            return Response({'error': 'Full course not found'}, status=status.HTTP_404_NOT_FOUND)
        videolist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#=======================Library===================================
class CategoryBook(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        queryset = BookCategory.objects.prefetch_related('books').all()
        serializer = BookCategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== Detail Book category ==================================
class CategoryBookDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return BookCategory.objects.get(pk=pk)
        except BookCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({'error': 'book category not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = BookCategorySerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        bookcategory = self.get_object(pk)
        if bookcategory is None:
            return Response({'error': 'update book category not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = BookCategorySerializer(bookcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookcategory = self.get_object(pk)
        if bookcategory is None:
            return Response({'error': 'delete book category not found'}, status=status.HTTP_404_NOT_FOUND)
            
        bookcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ================================ Book ===============================================
class BookLibrary(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        books = Book.objects.select_related('book_category_name').all()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer=BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#================================bookLibrary detail================================
class BookLibraryDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self , pk):
        try:
            return BookCategory.objects.get(pk=pk)
        except BookCategory.DoesNotExist:
            return None
        
    def get(self,request,pk):
        books=self.get_object(pk)
        if books is None :
            return Response({'error': 'book  not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookCategorySerializer(books, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        books = self.get_object(pk)
        if books is None:
            return Response({'error': 'update book  not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = BookCategorySerializer(books, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,  pk):
        books = self.get_object(pk)
        if books is None:
            return Response({'error': 'delete book y not found'}, status=status.HTTP_404_NOT_FOUND)   
        books.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#================notification=================================
class NotificationApp(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request) :
        nottification= Notification.objects.all()
        serializer = NotificationSerializer(nottification, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer= NotificationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )

        





        
    
         
           
    
             
        

