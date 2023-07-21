from rest_framework.views import APIView
from rest_framework import generics,status
from AdminUser.models import User
from QuizApp.models import Quiz
from QuizApp.serializers import QuizListSerializer
from .serializers import UserSerializer,RegisterSerializer,UserProfileSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from AdminUser.pagination import CustomPagination
from django.contrib.auth import logout


class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return Response({"message":"User created."})
        else:
            return Response(serializer.errors)


class UserListCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save()

    def post(self,request,*args,**kwargs):
        response=super().post(request,*args,**kwargs)
        return Response({"message":"Created New User",'status':200})



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        logout(request)
        return Response({'message':'Logout Successful'},status=status.HTTP_200_OK)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser,]

    def put(self,request,*args,**kwargs):
        return Response({'message':'User Updated'})

    def patch(self,request,*args,**kwargs):
        return Response({'message':'User Updated'})

    def delete(self,request,*args,**kwargs):
        return Response({'message':'User Deleted'})


class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        user_serializer=self.serializer_class(request.user)
        quiz_queryset=Quiz.objects.filter(creator=request.user)
        quiz_serializer=QuizListSerializer(quiz_queryset,many=True)
        response_data={
            "username":user_serializer.data["username"],
            "email":user_serializer.data["email"],
            "quizzes_created":quiz_serializer.data
        }
        return Response(response_data)

# Create your views here.
