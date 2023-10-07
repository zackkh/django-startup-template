from accelerator.builder.decorators import register_view, register_viewset
from django.urls import include, path
from django.views import generic

# Register your urls here
urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path(
        "auth/password/reset/confirm/<str:uidb64>/<str:token>/",
        generic.TemplateView.as_view(),
        name="password_reset_confirm",
    ),
    path("auth/register/", include("dj_rest_auth.registration.urls")),
]

urlpatterns += register_view.get_urls()
urlpatterns += register_viewset.get_urls()
