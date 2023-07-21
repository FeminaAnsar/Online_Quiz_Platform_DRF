from rest_framework import serializers
from AdminUser.models import User
from QuizApp.models import Quiz, Question, Answer,UserResponse,UserQuizScore
from AdminUser.serializers import UserSerializer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id','choice','answer_text','is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers=AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id','question_test','answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    creator=UserSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'

        def create(self,validated_data):
            questions_data=validated_data.pop('questions')
            quiz=Quiz.objects.create(**validated_data)
            for question_data in questions_data:
                answers_data=question_data.pop('answers')
                question=Question.objects.create(quiz=quiz,**question_data)
                for answer_data in answers_data:
                    Answer.objects.create(question=question,**answer_data)
            return quiz


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['id','topic','title','difficulty_level','date_created']


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['id','choice','answer_text']


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers=QuizAnswerSerializer(many=True)

    class Meta:
        model=Question
        fields=['id','question_text','answers']


class QuizTakingSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['title','questions']

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserResponse
        fields='__all__'


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserResponse
        fields='__all__'


class UserQuizScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserQuizScore
        fields='__all__'


class QuizAnalyticsSerializer(serializers.ModelSerializer):
    total_quizzes=serializers.SerializerMethodField()
    total_quiz_takers=serializers.SerializerMethodField()
    average_quiz_score=serializers.SerializerMethodField()
    performance_metrics=serializers.SerializerMethodField()
    question_statistics=serializers.SerializerMethodField()

    class Meta:
        model=Quiz
        fields=['id','title','total_quizzes','total_quiz_takers',
            'average_quiz_score','pass_percentage','performance_metrics','question_statistics']

        def get_total_quizzes(self,obj):
            return Quiz.objects.count()

        def get_total_quiz_takers(self,obj):
            return UserQuizScore.objects.filter(quiz=obj).values('user').distinct().count()

        def get_average_quiz_score(self,obj):
            quiz_scores=UserQuizScore.objects.filter(quiz=obj)
            total_scores=quiz_scores.count()
            if total_scores==0:
                return 0
            total_score_sum=sum(score.score for score in quiz_scores)
            return total_score_sum/total_scores

        def get_pass_percentage(self,obj):
            quiz_scores=UserQuizScore.objects.filter(quiz=obj)
            total_users=User.objects.count()
            if total_users==0:
                return 0
            pass_count=quiz_scores.filter(score__gte=40).count()
            return (pass_count/total_users) * 100

        def get_performance_metrics(self,obj):
            quiz_scores=UserQuizScore.objects.filter(quiz=obj)
            scores=quiz_scores.values('quiz').annotate(
                average_score=models.Avg('score'),
                highest_score=models.Max('score'),
                lowest_score=models.Min('score'),

            ).values('average_score','highest_score','lowest_score')
            return scores[0],scores[1] if scores else{
                'average_score':0,
                'highest_score':0,
                'lowest_score':0
            }
        def get_question_statistics(self,obj):
            return{
                'most_answered_questions':[],
                'least_answered_questions':[],
            }
