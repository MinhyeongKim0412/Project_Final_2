from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model

# 사용자 모델 커스터마이징 (로그인, 회원가입, 회원 정보 관리 등)
class CustomUser(AbstractUser):
    apartment_number = models.CharField(max_length=10, blank=True, null=True)

    # groups 필드 수정
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # 커스텀 유저 모델에 대한 고유한 이름
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        verbose_name='groups'
    )

    # user_permissions 필드 수정
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # 커스텀 유저 모델에 대한 고유한 이름
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

# 게시판 모델 (글 작성, 수정, 삭제, 조회 기능)
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
