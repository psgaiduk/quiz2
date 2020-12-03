from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from .models import Questions
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, login

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
    return render(request, 'result.html', {'score': score, 'lst': lst})


def save_ans(request):
    ans = request.GET['ans']
    lst.append(ans)


def welcome(request):
    lst.clear()
    return render(request, 'welcome.html')


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

    return render(request, 'showAnswer.html', {'score': score,
                                               'list_answer': list_answer, 'list_all': list_all})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):

        return super(RegisterFormView, self).form_invalid(form)


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
