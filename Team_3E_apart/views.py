from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # 로그인 필요 데코레이터 추가
from .forms import CustomUserCreationForm, PostForm, CommentForm  # 커스텀 사용자 생성 폼 및 게시글 작성을 위한 폼 import
from .models import CustomUser, Post, Comment  # Post 모델 import

def main(request):
    return render(request, 'main.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # 자동 로그인
            messages.success(request, f"{username}님 안녕하세요, 반갑습니다!")  # 로그인 성공 메시지
            return redirect('홈')  # 로그인 후 홈으로 리다이렉트 (적절한 URL 이름으로 변경)
        else:
            messages.error(request, "아이디 또는 비밀번호가 잘못되었습니다.")  # 로그인 실패 시 오류 메시지
    
    return render(request, 'login.html')  # GET 요청 시 로그인 페이지 반환

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # 커스텀 폼 인스턴스 생성
        if form.is_valid():
            user = form.save()  # 사용자 저장
            login(request, user)  # 자동 로그인
            messages.success(request, "회원가입이 완료되었습니다.")  # 회원가입 성공 메시지
            return redirect('홈')  # 가입 후 홈으로 리다이렉트
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})  # 폼 전달

def mypage_view(request):
    return render(request, 'mypage.html', {'user': request.user}) if request.user.is_authenticated else redirect('로그인')

def custom_logout_view(request):
    logout(request)  # 사용자를 로그아웃합니다.
    messages.success(request, '로그아웃되었습니다!')  # 성공 메시지를 추가합니다.
    return redirect('홈')  # 홈 화면으로 리다이렉트합니다.

def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()  # 사용자 삭제
        logout(request)  # 로그아웃
        messages.success(request, "로그아웃이 완료되었습니다.")  # 로그아웃 성공 메시지
        return redirect('main')  # 메인 페이지로 리다이렉트
    return render(request, 'delete_account.html')

# 비밀번호 재설정 요청 뷰
def find_account_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            # 커스텀 사용자 모델을 사용하여 사용자 찾기
            user = CustomUser.objects.get(username=username, email=email)
            return redirect('비밀번호재설정', username=user.username)  # 비밀번호 재설정 화면으로 이동
        except CustomUser.DoesNotExist:
            messages.error(request, '해당 아이디와 이메일이 일치하는 사용자를 찾을 수 없습니다.')
            return redirect('정보찾기')  # 다시 정보 찾기 페이지로 이동
    return render(request, 'find_account.html')

# 비밀번호 재설정 화면 뷰
def reset_password_view(request, username):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, '비밀번호가 성공적으로 재설정되었습니다.')
            return redirect('로그인')  # 로그인 페이지로 이동
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')

    return render(request, 'reset_password.html', {'username': username})

def board_view(request):
    posts = Post.objects.all()  # 모든 게시글 가져오기
    return render(request, 'board.html', {'posts': posts})

@login_required  # 로그인한 사용자만 접근 가능
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Post 객체 생성
            post.author = request.user  # 현재 사용자 지정
            post.save()  # 데이터베이스에 저장
            messages.success(request, '게시글이 성공적으로 작성되었습니다.')  # 작성 성공 메시지
            return redirect('게시판')  # 게시판으로 리다이렉트
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

@login_required  # 로그인한 사용자만 접근 가능
def post_edit_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 게시글 가져오기
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # 기존 게시글 인스턴스를 사용하여 폼 생성
        if form.is_valid():
            form.save()  # 수정사항 저장
            messages.success(request, '게시글이 성공적으로 수정되었습니다.')  # 수정 성공 메시지
            return redirect('글조회', post_id=post.id)  # 수정 후 게시글 보기로 리다이렉트
    else:
        form = PostForm(instance=post)  # GET 요청 시 기존 게시글 데이터로 폼 생성
    return render(request, 'post_edit.html', {'form': form, 'post': post})  # 수정 폼과 게시글 데이터 전달

def post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()  # 해당 게시물의 모든 댓글 가져오기

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # 현재 사용자 설정
            comment.save()
            return redirect('글조회', post_id=post.id)  # 새로 고침

    else:
        form = CommentForm()

    return render(request, 'post_view.html', {'post': post, 'comments': comments, 'form': form})

def post_reaction_view(request, post_id):
    return render(request, 'post_reaction.html')

@login_required  # 로그인한 사용자만 접근 가능
def update_profile_view(request):
    if request.method == 'POST':
        # 사용자 정보 수정
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        # 사용자 정보 업데이트
        request.user.username = username
        request.user.email = email
        
        if new_password:
            request.user.set_password(new_password)  # 새 비밀번호 설정
        
        request.user.save()  # 변경사항 저장
        messages.success(request, '회원정보가 성공적으로 수정되었습니다.')  # 성공 메시지
        return redirect('마이페이지')  # 수정 후 마이페이지로 리다이렉트
    return render(request, 'update_profile.html')  # GET 요청 시 수정 폼 반환
