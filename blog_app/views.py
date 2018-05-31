from django.shortcuts import render
from django.contrib.auth.models import *
from .models import *
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *
from django.views.generic import View

def homePage(request):
    try:
        posts = Artykul.objects.filter().order_by('-dataUtworzenia')[:10]
    except Artykul.DoesNotExist:
        return render(request, 'blog_app/home.html', {})
    else:
        return render(request, 'blog_app/home.html', {'posts': posts})


def loginPage(request):
    return render(request, 'blog_app/login.html', {})

def registerPage(request):
    return render(request, 'blog_app/register.html', {})

def blogPage(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        raise Http404

    try:
        posts = Artykul.objects.filter(autor = user).order_by('dataUtworzenia')
    except Artykul.DoesNotExist:
        raise Http404

    return render(request, 'blog_app/blog.html', {'posts': posts, 'userr': user})

def articlePage(request, id):
    try:
        post = Artykul.objects.get(pk = id)
    except Artykul.DoesNotExist:
        raise Http404
    return render(request, 'blog_app/article.html', {'post': post}) #, 'user': post.user

def userProfile(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return render(request, 'blog_app/home.html', {'message': "Nie istnieje użytkownik o podanej nazwie."})
        #raise Http404( 'Nie istnieje użytkownik o podanej nazwie.' )
    return render(request, 'blog_app/profile.html', {'userr': user})

class userRegister(View):
    def get(self, request):
        form = UserForm(None)
        return render(request, 'blog_app/register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return render(request, 'blog_app/home.html', {'message': "Rejestracja pomyślna."})

        else:
            return render(request, 'blog_app/register.html', {'form': form, 'message': "Błąd! Użytkownik o podanej nazwie już istnieje."})

# class userLogin(View):
#     def get(self, request):
#         form = LoginForm(None)
#         return render(request, 'blog_app/login.html', {'form': form})
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return render(request, 'blog_app/profile.html', {'user': user, 'message': "Rejestracja pomyślna."})
#         else:
#             return self.get()

def newArticle(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.autor = request.user
            post.dataUtworzenia = timezone.now()
            post.save()
            return redirect('articlePage' , id = post.id)
    else:
        form = ArticleForm
    return render(request, 'blog_app/editArticle.html', {'form': form})

def editArticle(request, id):
    post = get_object_or_404(Artykul, pk = id)
    if post.autor != request.user:
        return HttpResponse("Błąd! Nie możesz edytować artykułów innych użytkowników.")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.autor = request.user
            post.dataUtworzenia = timezone.now()
            post.save()
            return redirect('articlePage' , id = post.id)
    else:
        form = ArticleForm(instance = post)
    return render(request, 'blog_app/editArticle.html', {'form': form})

