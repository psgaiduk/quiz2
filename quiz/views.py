from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .models import Questions, QuizzComplete
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from django.contrib.auth.decorators import login_required

lst = []
answers = Questions.objects.all()
anslist = []

for i in answers:
    anslist.append(i.answer)


def index(request):
    obj = Questions.objects.all()
    count = Questions.objects.all().count()
    paginator = Paginator(obj, 1)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        questions = paginator.page(page)
    except(EmptyPage, InvalidPage):

        questions = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'obj': obj, 'questions': questions, 'count': count})


def result(request):
    score = 0
    for i in range(len(lst)):
        if lst[i] == anslist[i]:
            score += 1

    percent = score / len(lst)

    if percent > 0.75:
        ok = True
    else:
        ok = False

    user = request.user

    if len(QuizzComplete.objects.filter(student=user)) > 0:
        QuizzComplete.objects.filter(student=user).delete()

    QuizzComplete.objects.update_or_create(
        student=user,
        score=score,
        complete=ok,

    )
    return render(request, 'result.html', {'score': score, 'ok': ok})


def save_ans(request):
    ans = request.GET['ans']
    lst.append(ans)


def welcome(request):
    lst.clear()
    return render(request, 'welcome.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)


def show_answers(request):
    score = 0
    list_all = []
    obj = Questions.objects.all()
    for text in obj:
        list_all.append(text)
    list_answer = []
    for i in range(len(lst)):
        list_objects = {}
        list_objects['question'] = (list_all[i].uestion)
        list_objects['answer'] = (anslist[i])
        if lst[i] == anslist[i]:
            score += 1
            list_objects['right'] = (1)
        else:
            list_objects['right'] = (0)
        list_answer.append(list_objects)

    procent = score / len(list_answer)

    return render(request, 'showAnswer.html', {'score': score, 'procent': procent,
                                               'list_answer': list_answer, 'list_all': list_all})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES)
        if form.is_valid() and p_form.is_valid():
            user = form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            messages.success(request, f'Регистрации выполнена, можешь войти в аккаунт')
            return redirect('/login/')
    else:
        form = UserRegisterForm()
        p_form = ProfileUpdateForm(request.POST)
    return render(request, 'register.html', {'form': form, 'p_from': p_form})

# class RegisterFormView(FormView):
#     form_class = UserCreationForm
#     success_url = "/login/"
#     template_name = "register.html"
#
#     def form_valid(self, form):
#         form.save()
#         return super(RegisterFormView, self).form_valid(form)
#
#     def form_invalid(self, form):
#
#         return super(RegisterFormView, self).form_invalid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
