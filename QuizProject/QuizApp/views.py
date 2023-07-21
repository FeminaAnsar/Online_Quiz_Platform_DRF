from rest_framework.response import Response
from .models import Question,Quiz,UserResponse,Answer
from .serializers import (
    QuizListSerializer,QuizResultSerializer,QuizSerializer,QuizAnalyticsSerializer,QuizTakingSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from AdminUser.models import User
from AdminUser.pagination import CustomPagination
from django.db.models import Avg,Max,Min,Count
from rest_framework.views import APIView


class QuizListCreateView(generics.CreateAPIView):
    queryset=Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def post(self,request,*args,**kwargs):
        request.data['creator']=request.user.id
        response=super().post(request,*args,**kwargs)
        return Response({"message":"New Quiz Created"})


class UserQuizTakingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request,pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            serializer = QuizTakingSerializer(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response({'error':"Quiz not found."})

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            questions = quiz.questions.all()
            total_questions = questions.count()
            correct_answers = 0

            for question in questions:
                question_id = question.id
                selected_choice_id = request.data.get(str(question_id), None)
                if selected_choice_id is not None:
                    try:
                        selected_choice = Answer.objects.get(pk=selected_choice_id)
                    except Answer.DoesNotExist:
                        return Response({"error": "Selected answer not found"})

                    if selected_choice.is_correct:
                        correct_answers += 1

            score = (correct_answers / total_questions) * 100
            UserResponse.objects.create(user=request.user, quiz=quiz, score=score)
            return Response({"You are scored ": score})

        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found."})


class UserQuizScoreView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = QuizResultSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return UserResponse.objects.filter(user=user)



class QuizListView(generics.ListAPIView):
    queryset=Quiz.objects.all()
    pagination_class = CustomPagination
    serializer_class = QuizListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['topic','difficulty_level','created_at']


class QuizAnalyticsView(APIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        total_quizzes = Quiz.objects.count()
        total_quiz_takers = UserResponse.objects.values('user').distinct().count()
        average_quiz_score = UserResponse.objects.aggregate(avg_score=Avg('score'))['avg_score']

        quizzes = Quiz.objects.all()
        avg_scores_of_each_quiz = quizzes.annotate(avg_score=Avg('userresponse__score')).values('title', 'avg_score')
        highest_score = UserResponse.objects.aggregate(max_score=Max('score'))['max_score']
        lowest_score = UserResponse.objects.aggregate(min_score=Min('score'))['min_score']
        quiz_taken_counts = UserResponse.objects.values('quiz__title').annotate(quiz_count=Count('quiz'))

        question_responses_count = UserResponse.objects.values('quiz__questions__question_text').annotate(
            response_count=Count('quiz'))
        least_answered = question_responses_count.order_by('response_count')
        most_answered = question_responses_count.order_by('-response_count')
        most_answered_questions = [item['quiz__questions__question_text'] for item in most_answered]
        least_answered_questions = [item['quiz__questions__question_text'] for item in least_answered]

        total_users = User.objects.count()
        passed_users = UserResponse.objects.filter(score__gte=40).values('user').distinct().count()
        percentage_of_users = (passed_users / total_users) * 100

        Quiz_Overview = {
            'total_quizzes': total_quizzes,
            'total_quiz_takers': total_quiz_takers,
            'average_quiz_score': average_quiz_score,
        }

        Performance_Metrics = {
            'quiz_taken_counts': list(quiz_taken_counts),
            'average_scores': list(avg_scores_of_each_quiz),
            'highest_score': highest_score,
            'lowest_score': lowest_score,
        }

        Question_Statistics = {
            "most_answered_questions": most_answered_questions,
            "least_answered_questions": least_answered_questions
        }

        percentage = {
            "percentage_of_users_passed": percentage_of_users,
        }

        return Response(
            {
            'Quiz_Overview': Quiz_Overview,
            'Performance_Metrics': Performance_Metrics,
            'Question_Statistics': Question_Statistics,
            'percentage_of_users_passed': percentage
        }
        )

'''class PerformanceMetricsView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['performance_metrics']=True
        return context


class QuestionStatisticsView(generics.RetrieveAPIView):
    queryset=Quiz.objects.all()
    serializer_class = QuizAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['question_statistics']=True
        return context'''

# Create your views here.
