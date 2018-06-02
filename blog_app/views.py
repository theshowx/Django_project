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

    comments = Komentarz.objects.filter(artykul = post).order_by('dataZamieszczenia')
    answers = Komentarz_odpowiedz.objects.filter(artykul = post).order_by('dataZamieszczenia')

    return render(request, 'blog_app/article.html', {'post': post, 'comments': comments, 'answers': answers}) #, 'user': post.user

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
    return render(request, 'blog_app/editArtCom.html', {'form': form, 'header': "Dodaj nowy artykuł."})

def editArticle(request, id):
    post = get_object_or_404(Artykul, pk = id)
    if post.autor != request.user:
        return HttpResponse("Błąd! Nie możesz edytować artykułów innych użytkowników.")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.autor = request.user
            #post.dataUtworzenia = timezone.now()
            post.save()
            return redirect('articlePage' , id = post.id)
    else:
        form = ArticleForm(instance = post)
    return render(request, 'blog_app/editArtCom.html', {'form': form, 'header': "Zedytuj swój artykuł."})

def deleteArticle(request, id):
    post = get_object_or_404(Artykul, pk = id)
    if post.autor != request.user:
        return HttpResponse("Błąd! Nie możesz usuwać artykułów innych użytkowników.")

    post.delete()
    return redirect('blogPage' , username = request.user.username)

def newComment(request, id):
    post = get_object_or_404(Artykul, pk = id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.autor = request.user
            comment.dataZamieszczenia = timezone.now()
            comment.artykul = post
            comment.save()
            return redirect('articlePage' , id = post.id)
    else:
        form = CommentForm
    return render(request, 'blog_app/editArtCom.html', {'form': form, 'header': "Dodaj nowy komentarz."})

def editComment(request, idArt, idKom):
    comment = get_object_or_404(Komentarz, pk = idKom)
    if comment.autor != request.user:
        return HttpResponse("Błąd! Nie możesz edytować komentarzy innych użytkowników.")

    post = get_object_or_404(Artykul, pk = idArt)

    if request.method == "POST":
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.autor = request.user
            #comment.dataZamieszczenia = timezone.now()
            comment.artykul = post
            comment.save()
            return redirect('articlePage' , id = post.id)
    else:
        form = CommentForm(instance = comment)
    return render(request, 'blog_app/editArtCom.html', {'form': form, 'header': "Zedytuj swój komentarz."})

def deleteComment(request, idArt, idKom):
    comment = get_object_or_404(Komentarz, pk = idKom)
    if comment.autor != request.user:
        return HttpResponse("Błąd! Nie możesz usuwać komentarzy innych użytkowników.")

    answers = Komentarz_odpowiedz.objects.filter(komentarz = comment).order_by('dataZamieszczenia')

    if answers:
        for answer in answers:
            answer.odpowiedz.delete()

    comment.delete()
    return redirect('articlePage' , id = idArt)

def addAnswer(request, idArt, idKom):
    post = get_object_or_404(Artykul, pk = idArt)
    comment = get_object_or_404(Komentarz, pk = idKom)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.autor = request.user
            answer.artykul = post
            answer.dataZamieszczenia = timezone.now()
            answer.czyOdpowiedz = True
            answer.save()

            comment_answer = Komentarz_odpowiedz.create(comment, answer, post)
            comment_answer.dataZamieszczenia = timezone.now()
            comment_answer.save()

            return redirect('articlePage' , id = post.id)

    else:
        form = CommentForm
        return render(request, 'blog_app/editArtCom.html', {'form': form, 'header': "Dodaj nowy komentarz."})

