from content.models import Note, Experience
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser


def home(request):
    if request.user.is_authenticated:
        return redirect('/courses')
    else:
        return render(request, "users/index.html")


class UserCreate(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    template_name = "users/register.html"
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        valid = super(UserCreate, self).form_valid(form)
        user = self.object
        login(self.request, user)
        return valid


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes-list.html'

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
    template_name = 'exps-list.html'

    def get_queryset(self):
        return Experience.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['res_class'] = 'experience'
        return context
