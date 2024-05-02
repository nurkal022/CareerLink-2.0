from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("service", views.service, name="service"),
    path(
        "choose_specialization",
        views.choose_specialization,
        name="choose_specialization",
    ),
    path("team", views.team, name="team"),
    path("project", views.project, name="project"),
    path("not_found", views.not_found, name="not_found"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("test/<int:spec_id>/", views.test_view, name="test"),
    path("test/<int:spec_id>/submit/", views.submit_test, name="submit_test"),
    path("candidates/<int:spec_id>/", views.view_candidates, name="view_candidates"),
    path("profile/edit/", views.candidate_profile, name="profile_edit"),
    path("profile/", views.profile_view, name="profile_view"),
]
