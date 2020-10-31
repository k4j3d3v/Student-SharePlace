from content.forms import AddNoteModelForm, AddExperienceModelForm
from content.models import Note, Experience
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView


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
