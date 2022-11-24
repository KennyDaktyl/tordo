from django.urls import path

from .views import first_page, privacy_policy, terms_rules

urlpatterns = [
    path("", first_page, name="front_page"),
    path("polityka-prywatnosci", privacy_policy, name="privacy_policy"),
    path("regulamin", terms_rules, name="terms"),
]