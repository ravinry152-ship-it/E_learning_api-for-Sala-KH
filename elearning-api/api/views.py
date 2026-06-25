from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    CourseName, FullCourse, 
    BookCategory, Book,Videolist,
    Notification,
    Question,
    Quiz,
    Choice,
    QuizSubmission,
)
from django.contrib.auth.models import User
from dj_rest_auth.registration.views import SocialLoginView # pyright: ignore[reportMissingImports]
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .serializer import (
    CourseNameSerializer, FullCourseSerializer,
    VideoListSerializer,BookCategorySerializer,
    BookSerializer,NotificationSerializer,
    QuizSerializer,QuestionSerializer,
    ChoiceSerializer,QuizSubmissionSerializer
)
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
#======================Login and Signup  with  socail media=======================
# 1. Google Login View
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/accounts/google/login/callback/" 
    client_class = OAuth2Client

# 2. Facebook Login View
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

# 3. GitHub Login View
class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/accounts/github/login/callback/"
    client_class = OAuth2Client
#=========================Course Category=========================================           
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

class FullCourselist(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        maincourse_id = request.query_params.get(
            'maincourse_id'
        )

        if maincourse_id:
            full_courses = FullCourse.objects.filter(
                maincourse_name_id=maincourse_id
            )
        else:
            full_courses = FullCourse.objects.all()

        serializer = FullCourseSerializer(
            full_courses,
            many=True,
            context={'request': request}
        )

        return Response({
            "full_courses": serializer.data
        })
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

        #  Filter តាម ID របស់ FullCourse (Ex: Python Full Course ID = 1)
        course_id = request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        #  Filter តាមឈ្មោះប្រភេទធំ (course_name = Programming ឬ Design)
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
    
#===========================question Test for lesson======================
class QuizTest(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        lesson_id = request.query_params.get('lesson_id')

        quizzes = Quiz.objects.all()

        if lesson_id:
            quizzes = quizzes.filter(lesson_id=lesson_id)

        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    def post(self ,request) :
        serializer = QuizSerializer(data= request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors, "error")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizTestDetail(APIView) :
    def get_object(self, pk):
        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return None
        
    def put(self, request,pk):
        quiz = self.get_object(pk)
        if  quit is None :
          return Response({'error': 'update book category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuizSerializer(quiz, data= request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,  pk):
        quit = self.get_object(pk)
        if quit is None:
            return Response({'error': 'delete quiz not found'}, status=status.HTTP_404_NOT_FOUND)   
        quit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class QuestionTest(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # ១. ចាប់យក lesson_id ពី URL Parameter (?lesson_id=3)
        lesson_id = request.query_params.get('lesson_id')

        if lesson_id:
            # ២. ទាញយកគ្រប់ Quiz ID ទាំងឡាយណាដែលបង្កើតឡើងសម្រាប់ Lesson ID នេះ
            quiz_ids = Quiz.objects.filter(lesson_id=lesson_id).values_list('id', flat=True)
            
            # ៣. Filter យកតែសំណួរណាដែលមាន quiz_id ស្ថិតនៅក្នុងលទ្ធផលខាងលើ
            questions = Question.objects.filter(quiz_id__in=quiz_ids)
            
            #  សម្រាប់ Debug មើលលើ Terminal របស់ Django
            print(f" Local Test -> Lesson ID: {lesson_id} | រកឃើញ Quiz IDs: {list(quiz_ids)} | ចំនួនសំណួរ: {questions.count()}")
        else:
            # បើគ្មានការបញ្ជូន lesson_id មកទេ ឱ្យបង្ហាញទាំងអស់
            questions = Question.objects.all()

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    def post(self,request) :
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors, "error")
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class QuestionTestDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self ,pk):
        try :
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist :
            return None
    
    def put(self ,request, pk) :
        question = self.get_object(pk)
        if question is None :
            return Response({'error': 'update Question not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(question, data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk) :
        question =self.get_object(pk)
        if question is None :
             return Response({'error': 'delete quiztion not found'}, status=status.HTTP_404_NOT_FOUND)   
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChoiceTest(APIView) :
    permission_classes = [IsAuthenticated]
    def get(self, request):
        #in model រសេរតែ lesson ប៉ុណ្ណោះ ប៉ុន្តែ Django បង្កើត Field មួយទៀតក្នុង Database ដោយស្វ័យប្រវត្តិឈ្មោះ:lesson_id
        #ទៅរក parameter ឈ្មោះ lesson_id ក្នុង URL ហើយយកតម្លៃរបស់វាមក
        lesson_id = request.query_params.get('lesson_id')
        choices = Choice.objects.all()
        if lesson_id:
            choices = choices.filter(
                question__quiz__lesson_id=lesson_id # Choice → Question → Quiz → យក lesson_id
                #ដេីម្បីJOIN Table ទាំង 3 ដោយស្វ័យប្រវត្តិ ដើម្បីរក Choice ដែលស្ថិតក្នុង Lesson ជាក់លាក់មួយ
            )

        serializer = ChoiceSerializer(
            choices,
            many=True
        )

        return Response(serializer.data)
    
    def post(self, request) :
        serializer = ChoiceSerializer(data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChoiceTestDetail(APIView) :
    permission_classes = [IsAuthenticated]
    def get_object(self, pk) :
        try :
            return Choice.objects.get(pk=pk)
        except Choice.DoesNotExist :
            return None
        
    def put(self ,request,pk) :
        choice = self.get_object(pk)
        if choice is None :
            return Response({'error': 'update Choice not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChoiceSerializer(choice, data = request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,pk) :
        choice =self.get_object(pk)
        if choice is None :
             return Response({'error': 'delete quiztion not found'}, status=status.HTTP_404_NOT_FOUND)   
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuizSubmissionTest(APIView) :
    permission_classes = [IsAuthenticated]
    def get(self, request) :
       try :
          quiz_submissions = QuizSubmission.objects.filter(user=request.user).order_by('-submitted_at')
          serializer = QuizSubmissionSerializer(quiz_submissions, many=True)
          return Response(serializer.data, status=status.HTTP_200_OK)
       except Exception as e :
           print(f" Error fetching submissions: {e}")
           return Response({"error": "មិនអាចទាញយកប្រវត្តិពិន្ទុបានទេ"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
    def post(self, request):
        quiz_id = request.data.get('quiz_id')
        user_answers = request.data.get('answers', []) # ជាប្រភេទ List លទ្ធផលឆ្លើយ
        
        if not user_answers:
            return Response({"error": "មិនមានចម្លើយត្រូវបានផ្ញើមកទេ"}, status=status.HTTP_400_BAD_REQUEST)
        
        correct_answers_count = 0
        total_questions = len(user_answers)
        
        # រត់ Loop ផ្ទៀងផ្ទាត់ចម្លើយរបស់សិស្សជាមួយ Database
        for ans in user_answers:
            q_id = ans.get('question_id')
            c_id = ans.get('choice_id')
            
            #  ពិនិត្យមើលក្នុងប្រព័ន្ធថា តើ Choice ID នេះជាចម្លើយដែលត្រឹមត្រូវ (is_correct=True) របស់សំណួរនេះមែនទេ?
            #  ត្រូវផ្ទៀងផ្ទាត់ឈ្មោះ field 'is_correct' ឱ្យត្រូវតាម Choice Model របស់អ្នក
            is_correct = Choice.objects.filter(id=c_id, question_id=q_id, is_correct=True).exists()
            
            if is_correct:
                correct_answers_count += 1
                
        #  ៣. គណនាភាគរយពិន្ទុពេញ ១០០ ផ្អែកលើចំនួនឆ្លើយត្រូវ
        score = int((correct_answers_count / total_questions) * 100) if total_questions > 0 else 0
        
        try:
            #  ៤. បង្កើត និងរក្សាទុកសន្លឹកកិច្ចការចូលទៅក្នុង QuizSubmission Model
            #  ប្រសិនបើប្រើ AllowAny ហើយមិនទាន់មាន User Login ទេ អាចជំនួស request.user ដោយ User គំរូណាមួយសិនដើម្បីតេស្ត
            submission = QuizSubmission.objects.create(
                user=request.user if request.user.is_authenticated else None, 
                quiz_id=quiz_id, # ភ្ជាប់ទៅកាន់ ID វិញ្ញាសា/មេរៀន
                score=score,
                total_questions=total_questions,
                correct_answers=correct_answers_count
            )
            
            #  ហុចលទ្ធផលពិន្ទុដែលគណនារួចត្រឡប់ទៅឱ្យ Flutter
            return Response({
                "score": score,
                "total_questions": total_questions,
                "correct_answers": correct_answers_count,
                "message": "ប្រឡង និងរក្សាទុកពិន្ទុជោគជ័យ!"
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f" Error saving submission: {e}")
            return Response({"error": "ការរក្សាទុកពិន្ទុចូល Database មានបញ្ហា"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

    





       

       
        





        





        
    
         
           
    
             
        

