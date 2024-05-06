from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
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


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "thank_you_page"
            )  # Перенаправление на страницу благодарности
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


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
        for question in Question.objects.filter(specialization=specialization):
            user_answer_id = request.POST.get(f"question_{question.id}")
            user_answers[question.id] = int(user_answer_id) if user_answer_id else None
            choice = question.choices.get(pk=user_answer_id)
            if choice.is_correct:
                correct_answers_count += 1
            questions_detail.append(
                {
                    "question": question.text,
                    "your_answer": choice.text,
                    "is_correct": choice.is_correct,
                }
            )

        total_questions = specialization.questions.count()
        attempt = TestAttempt.objects.create(
            candidate=Candidate.objects.get(user=request.user),
            specialization=specialization,
            correct_answers=correct_answers_count,
            total_questions=total_questions,
        )
        wrong_answers_count = total_questions - correct_answers_count

        context = {
            "specialization": specialization,
            "total_questions": total_questions,
            "correct_answers_count": correct_answers_count,
            "wrong_answers_count": wrong_answers_count,
            "percentage_correct": (correct_answers_count / total_questions) * 100,
            "questions_detail": questions_detail,
            "passed": attempt.passed(),
        }

        return render(request, "main/test_results.html", context)
    else:
        return redirect("test", spec_id=spec_id)


def view_candidates(request, spec_id):
    specialization = get_object_or_404(Specialization, pk=spec_id)
    candidates = Candidate.objects.filter(specialization=specialization)
    return render(
        request,
        "main/view_candidates.html",
        {"specialization": specialization, "candidates": candidates},
    )


def submit_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactRequest.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )
            # Перенаправление на страницу с подтверждением или обратно на контактную страницу с сообщением об успехе
            render(request, "contact.html", {"form": form})
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def profile_view(request):
    candidate, created = Candidate.objects.get_or_create(
        user=request.user, defaults={"specialization": None}
    )
    return render(request, "main/profile_view.html", {"candidate": candidate})


def specialization_detail(request, spec_id):
    specialization = get_object_or_404(Specialization, pk=spec_id)
    attempts = TestAttempt.objects.filter(specialization=specialization)

    total_attempts = attempts.count()
    passed_attempts = sum(1 for attempt in attempts if attempt.passed())
    failed_attempts = total_attempts - passed_attempts

    context = {
        "specialization": specialization,
        "total_attempts": total_attempts,
        "passed_attempts": passed_attempts,
        "failed_attempts": failed_attempts,
        "attempts": attempts,
    }
    return render(request, "main/specialization_detail.html", context)


@login_required
def candidate_profile(request):
    candidate, created = Candidate.objects.get_or_create(user=request.user)
    user_form = CustomUserEditForm(request.POST or None, instance=request.user)
    candidate_form = CandidateProfileForm(
        request.POST or None, request.FILES or None, instance=candidate
    )

    if request.method == "POST":
        if user_form.is_valid() and candidate_form.is_valid():
            user_form.save()
            candidate_form.save()
            messages.success(request, "Профиль успешно обновлен.")
            return redirect("profile_view")

    return render(
        request,
        "main/candidate_profile.html",
        {"user_form": user_form, "candidate_form": candidate_form},
    )
