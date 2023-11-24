from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import CreateView
from django.conf import settings

from .forms import CookCreationForm, CookSearchForm, CookForm
from .models import Cook


class SignUpView(CreateView):
    form_class = CookCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class RememberMeLoginView(View):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        username = request.session.pop("remember_me_username", "")
        password = request.session.pop("remember_me_password", "")
        form = AuthenticationForm(initial={"username": username, "password": password})
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            remember_me = request.POST.get("remember_me")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    self.request.session.set_expiry(
                        settings.SESSION_COOKIE_AGE
                    )
                else:
                    self.request.session.set_expiry(0)

                return redirect("/")

        return render(request, self.template_name, {"form": form})


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(initial={"username": name})
        return context

    def get_queryset(self):
        self.queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all()


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookForm

    def get_success_url(self):
        return reverse_lazy("users:cook-detail", kwargs={"pk": self.object.id})


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("users:cook-list")
