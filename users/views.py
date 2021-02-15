from content.models import Note, Experience
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        base_url = {
            'logout': 'Logout',
            'password_change': 'Change Password',
            'notes': 'Your Notes',
            'experiences': 'Your Experiences',
            'content:course-list': 'Your Courses',
            'edit_profile': 'Edit your profile!',
            'content:purchased-list': 'Purchased Notes',
            'content:note-request': 'Exchange Request',
            'content:notifications': 'Notifications'
        }
        return render(request, "users/dashboard.html", {'urls': base_url})
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

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)
    #
    # def get_form_kwargs(self):
    #     kwargs = super(NoteCreate, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('edit_profile')

    def get_object(self):
        return self.request.user


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    # context_object_name = 'resources'
    template_name = 'tables.html'

    # template_name = 'users/resource_list.html'

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
    template_name = 'tables-exp.html'

    # template_name = 'users/resource_list.html'

    def get_queryset(self):
        return Experience.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['res_class'] = 'experience'
        return context
