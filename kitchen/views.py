from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.template.loader import render_to_string


from .forms import (
    DishTypeSearchForm,
    CookSearchForm,
    DishSearchForm,
    DishForm,
    CookCreationForm,
    CookForm,
)
from .models import DishType, Dish, Cook


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


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
        #
        # form.fields['username'].widget.attrs['placeholder'] = 'Username'
        # form.fields['password'].widget.attrs['placeholder'] = 'Password'

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
                    self.request.session.set_expiry(1209600)
                else:
                    self.request.session.set_expiry(0)

                return redirect("/")

        return render(request, self.template_name, {"form": form})


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dishtype_list"
    template_name = "kitchen/dishtype_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        self.queryset = DishType.objects.all().order_by("name")
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dishtype-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dishtype-list")

    def get_success_url(self):
        page_number = self.request.GET.get("page")

        if page_number:
            query_params = QueryDict(mutable=True)
            query_params["page"] = page_number

            success_url = (
                reverse_lazy("kitchen:dishtype-list") + "?" + query_params.urlencode()
            )
        else:
            success_url = self.success_url

        return success_url


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType

    def get_success_url(self):
        referer = self.request.META.get("HTTP_REFERER")
        if referer:
            return referer
        return self.success_url


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5
    template_name = "kitchen/dish_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        context["sort_by"] = self.request.GET.get("sort_by", "name")
        return context

    def get_queryset(self):
        queryset = Dish.objects.all()

        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])

        sort_by = self.request.GET.get('sort_by', 'name')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'price':
            queryset = queryset.order_by('price')
        elif sort_by == 'dish_type':
            queryset = queryset.order_by('dish_type__name')

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html_content = render_to_string(self.template_name, context)

            print(f'HTML Content: {html_content}')

            return JsonResponse({'html_content': html_content})
        else:
            return super().render_to_response(context, **response_kwargs)
    # def render_to_response(self, context, **response_kwargs):
    #     if self.request.is_ajax():
    #         html_content = render_to_string(self.template_name, context)
    #         return JsonResponse({'html_content': html_content})
    #     else:
    #         return super().render_to_response(context, **response_kwargs)


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()

        ingredients = self.request.POST.getlist("ingredients")
        self.object.ingredients.set(ingredients)
        cooks = self.request.POST.getlist("cooks")
        self.object.cooks.set(cooks)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("kitchen:dish-detail", kwargs={"pk": self.object.id})


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["ingredients"].initial = self.object.ingredients.all()
        form.fields["cooks"].initial = self.object.cooks.all()

        return form

    def form_valid(self, form):
        self.object = form.save()

        ingredients = self.request.POST.getlist("ingredients")
        self.object.ingredients.set(ingredients)
        cooks = self.request.POST.getlist("cooks")
        self.object.cooks.set(cooks)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("kitchen:dish-detail", kwargs={"pk": self.object.id})


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


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
    # queryset = Cook.objects.prefetch_related("dishes__dish_type")


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookForm

    def get_success_url(self):
        return reverse_lazy("kitchen:cook-detail", kwargs={"pk": self.object.id})


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    if Dish.objects.get(id=pk) in cook.dishes.all():
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
