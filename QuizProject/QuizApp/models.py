from django.db import models
from AdminUser.models import User


class Quiz(models.Model):
    DIFFICULTY_CHOICES=[('easy','Easy'),
                        ('medium','Medium'),
                        ('hard','Hard'),
                        ]
    topic=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    difficulty_level= models.CharField(max_length=10,choices=DIFFICULTY_CHOICES,default='easy')
    date_created=models.DateTimeField(auto_now_add=True)

''' 

    def calculate_average_score(self):
        quiz_scores=UserQuizScore.objects.filter(quiz=self)
        total_scores=quiz_scores.count()
        if total_scores==0:
            return 0
        total_score_sum=sum(score.score for score in quiz_scores)
        return total_score_sum/total_scores

    def calculate_pass_percentage(self):
        quiz_scores=UserQuizScore.objects.filter(quiz=self)
        total_users=User.objects.count()
        if total_users==0:
            return 0
        pass_count=quiz_scores.filter(score__gte=self.passing_score).count()
        return(pass_count/total_users)*100'''


class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    question_text=models.CharField(max_length=255)


class Answer(models.Model):
    CHOICES= [
        ('a','Option A'),
        ('b','Option B'),
        ('c','Option C'),
        ('d','Option D')
    ]
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    answer_text=models.CharField(max_length=255)
    choice=models.CharField(max_length=1,choices=CHOICES)
    is_correct=models.BooleanField(default=False)


class UserResponse(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score=models.DecimalField(max_digits=5,decimal_places=2)
    date_taken = models.DateTimeField(auto_now_add=True)








# Create your models here.
