from content.models import Note, Experience
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from users.forms import CustomUserCreationForm


# Create your views here.

def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = form.cleaned_data['email'] if not user.username else user.username
            login(request, user)
            return redirect(reverse("users:dashboard"))
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    # context_object_name = 'resources'
    template_name = 'users/resource_list.html'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['res_class'] = 'note'
        return context


class ExperiencesListView(LoginRequiredMixin, ListView):
    model = Experience
    # context_object_name = 'resources'
    template_name = 'users/resource_list.html'

    def get_queryset(self):
        return Experience.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['res_class'] = 'experience'
        return context
