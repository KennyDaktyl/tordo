from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .functions import mobile


class FirstPage(TemplateView):
    template_name = "front/desktop/first_page.html"

    def get_template_names(self):
        if mobile(self.request):
            self.template_name = self.template_name.replace("desktop", "mobile")
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PrivacyPolicyPage(View):
    def get(self, request):
        template_name = "front/desktop/privacy_policy.html"
        ctx = {}
        if mobile(request):
            template_name = template_name.replace("desktop", "mobile")
        return render(request, template_name, ctx)


class TermsAndRulesPage(View):
    def get(self, request):
        template_name = "front/desktop/terms_rules.html"
        ctx = {}
        if mobile(request):
            template_name = template_name.replace("desktop", "mobile")
        return render(request, template_name, ctx)


first_page = FirstPage.as_view()
terms_rules = TermsAndRulesPage.as_view()
privacy_policy = PrivacyPolicyPage.as_view()
