from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, QueryDict
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .forms import (
    DishTypeSearchForm,
    DishSearchForm,
    DishForm,
)
from .models import DishType, Dish
from users.models import Cook


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_cooks = Cook.objects.count()
        num_dishes = Dish.objects.count()
        num_dish_types = DishType.objects.count()

        context.update({
            "num_cooks": num_cooks,
            "num_dishes": num_dishes,
            "num_dish_types": num_dish_types,
        })

        return context


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
        queryset = DishType.objects.all().order_by("name")
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


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

        sort_by = self.request.GET.get("sort_by", "name")
        sort_by_dict = {
            "name": "name",
            "price": "price",
            "dish_type": "dish_type__name",
        }

        sort_by_keyword = sort_by_dict.get(sort_by)
        if sort_by_keyword is not None:
            queryset = queryset.order_by(sort_by_keyword)

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish

    def post(self, request, *args, **kwargs):
        dish = self.get_object()
        cook = self.request.user

        if dish.cooks.filter(id=cook.id).exists():
            dish.cooks.remove(cook)
        else:
            dish.cooks.add(cook)

        return redirect("kitchen:dish-detail", pk=dish.pk)


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
