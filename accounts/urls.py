"""
path('', views.home, name='home')
path('', Home.as_view(), name='home')
path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import v_signup_view, v_homepage, v_logout_view, v_profile

app_name = "accounts"


urlpatterns = [
    path("profile/", v_homepage, name="homepage"),
    path("details/", v_profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", v_logout_view, name="logout"),
    path("signup/", v_signup_view, name="signup"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

