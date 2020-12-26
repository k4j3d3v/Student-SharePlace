from content.forms import AddNoteModelForm, AddExperienceModelForm
from content.models import Note, Experience, Course
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from users.models import CustomUser


class ExperienceUpdate(UpdateView):
    model = Experience
    form_class = AddExperienceModelForm
    template_name = 'content/note_update_form.html'
    # success_url = '/books/'


class ExperienceDelete(DeleteView):
    model = Experience
    success_url = reverse_lazy('experiences')
    template_name = 'content/note_confirm_delete.html'


class ExperienceDetail(DetailView):
    model = Experience


class ExperienceCreate(LoginRequiredMixin, CreateView):
    form_class = AddExperienceModelForm
    template_name = 'content/note_add.html'
    success_url = reverse_lazy('experiences')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NoteUpdate(UpdateView):
    model = Note
    form_class = AddNoteModelForm
    template_name_suffix = '_update_form'
    # success_url = '/books/'


class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('notes')


class NoteDetail(DetailView):
    model = Note


class NoteCreate(LoginRequiredMixin, CreateView):
    form_class = AddNoteModelForm
    template_name = 'content/note_add.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = AddNoteModelForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return HttpResponse('/thanks/')
    #
    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = AddNoteModelForm()
    #
    # return render(request, 'content/note_add.html', {'form': form})


class CoursesListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses_list'
    template_name = 'content/course_list.html'

    def get_queryset(self):
        # TODO: fix missing degree field in admin user
        print("email: %s \n" % self.request.user.email)
        user = CustomUser.objects.get(email=self.request.user.email)
        print("User: %s" % (dir(user)))
        return Course.objects.filter(degree=user.degree)

    # TODO: https://docs.djangonoteproject.com/en/3.1/topics/db/examples/
    # start from here
    # def get_context_data(self, **kwargs):
    # #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     user = CustomUser.objects.get(email=self.request.user.email)
    # #     courses = Course.objects.filter(degree=user.degree)
    # #     # Add in a QuerySet of all the books
    #     # context['res_count'] =
    #     return context
