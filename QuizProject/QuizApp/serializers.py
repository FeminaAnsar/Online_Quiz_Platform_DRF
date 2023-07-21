from rest_framework import serializers
from QuizApp.models import Quiz, Question, Answer,UserResponse
from AdminUser.serializers import UserSerializer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id','choice','answer_text','is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers=AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id','question_text','answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,read_only=True)
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
        model=Answer
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



