from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.


def home(request):
    return render(request, "main/index.html")


def about(request):
    return render(request, "main/about.html")


def service(request):
    return render(request, "main/service.html")


def contact(request):
    return render(request, "main/contact.html")


def team(request):
    return render(request, "main/team.html")


def project(request):
    return render(request, "main/project.html")


def not_found(request):
    return render(request, "main/404.html")


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomAuthenticationForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "main/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Сәтті кірдіңіз!")
                return redirect(
                    "home"
                )  # Перенаправляем на главную страницу после успешного входа
            else:
                messages.error(request, "Қате пайдаланушы аты немесе құпия сөз.")
    else:
        form = CustomAuthenticationForm()

    return render(request, "main/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


def choose_specialization(request):
    specializations = Specialization.objects.all()
    return render(
        request, "main/choose_specialization.html", {"specializations": specializations}
    )


def test_view(request, spec_id):
    specialization = get_object_or_404(Specialization, pk=spec_id)
    return render(request, "main/test.html", {"specialization": specialization})


@login_required
def submit_test(request, spec_id):
    specialization = get_object_or_404(Specialization, pk=spec_id)
    user_answers = {}
    correct_answers_count = 0
    questions_detail = []

    if request.method == "POST":
        # Сбор ответов пользователя и подсчет правильных ответов
        for question in specialization.questions.all():
            user_answer_id = request.POST.get(f"question_{question.id}")
            user_answers[question.id] = int(user_answer_id) if user_answer_id else None
            if user_answer_id:
                choice = question.choices.get(pk=user_answer_id)
                is_correct = choice.is_correct
                questions_detail.append((question.text, choice.text, is_correct))
                if is_correct:
                    correct_answers_count += 1

        total_questions = specialization.questions.count()
        wrong_answers_count = total_questions - correct_answers_count
        percentage_correct = (correct_answers_count / total_questions) * 100

        if percentage_correct >= 80:
            # Обновление или создание кандидата в зависимости от существования записи
            candidate, created = Candidate.objects.update_or_create(
                user=request.user, defaults={"specialization": specialization}
            )
            if created:
                message = "Congratulations! You have successfully passed the test and are now registered as a candidate."
            else:
                message = "Congratulations! Your specialization has been updated."
            messages.success(request, message)
        else:
            messages.error(
                request, "Unfortunately, you did not pass the test. Please try again."
            )

        # Передача результатов теста на страницу результатов
        context = {
            "total_questions": total_questions,
            "correct_answers_count": correct_answers_count,
            "wrong_answers_count": wrong_answers_count,
            "percentage_correct": percentage_correct,
            "questions_detail": questions_detail,
            "specialization": specialization,
        }
        return render(request, "main/test_results.html", context)
    else:
        # Если метод не POST, отправить пользователя на страницу теста
        return redirect("test", spec_id=spec_id)


def view_candidates(request, spec_id):
    specialization = get_object_or_404(Specialization, pk=spec_id)
    candidates = Candidate.objects.filter(specialization=specialization)
    return render(
        request,
        "main/view_candidates.html",
        {"specialization": specialization, "candidates": candidates},
    )


def profile_view(request):
    candidate, created = Candidate.objects.get_or_create(
        user=request.user, defaults={"specialization": None}
    )
    return render(request, "main/profile_view.html", {"candidate": candidate})


@login_required
def candidate_profile(request):
    candidate, created = Candidate.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CandidateProfileForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect("profile_view")  # Название URL для просмотра профиля
    else:
        form = CandidateProfileForm(instance=candidate)

    return render(request, "main/candidate_profile.html", {"form": form})
