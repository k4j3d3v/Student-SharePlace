from content.models import Note, Experience
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser


# Create your views here.

def dashboard(request):
    return render(request, "users/dashboard.html")


# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data['degree'])
#             user = form.save()
#             user.username = form.cleaned_data['email'] if not user.username else user.username
#             login(request, user)
#             return redirect(reverse("dashboard"))
#     else:
#         form = CustomUserCreationForm()
#
#     return render(request, "users/register.html", {"form": form})

class UserCreate(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    template_name = "users/register.html"
    success_url = reverse_lazy('dashboard')

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

    def get_object(self):
        return self.request.user


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
