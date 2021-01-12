import json

from content.forms import AddNoteModelForm, AddExperienceModelForm
from content.models import Note, Experience, Course
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
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

    def get_form_kwargs(self):
        kwargs = super(ExperienceCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # print(form.instance.degree)
        # for d in self.request.user.degree:
        #     form.instance.degree.add(d)
        return super().form_valid(form)


class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('notes')


class NoteDetail(DetailView):
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        user = CustomUser.objects.get(email=self.request.user.email)
        context['purchased'] = True if user.purchased_notes.filter(id=id) else False
        return context


# How to make a common superclass for NoteUpdate and NoteCreate views
# to accomplish DRY principle
# class NoteManipulate(View):
#     form_class = AddNoteModelForm
#     model = Note
#
#     def get_form_kwargs(self):
#         kwargs = super(NoteCreate, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs


class NoteUpdate(UpdateView):
    model = Note
    form_class = AddNoteModelForm
    template_name_suffix = '_update_form'

    # success_url = '/books/'

    def get_form_kwargs(self):
        kwargs = super(NoteUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NoteCreate(LoginRequiredMixin, CreateView):
    form_class = AddNoteModelForm
    template_name = 'content/note_add.html'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NoteCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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


def get_exact_match(model_class, m2m_field, ids):
    query = model_class.objects.all()
    for _id in ids:
        query = query.filter(**{m2m_field: _id})
    return query


class CoursesListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses_list'
    template_name = 'content/course_list.html'

    # def get_queryset(self):
    #     # TODO: fix missing degree field in admin user
    #     print("email: %s \n" % self.request.user.email)
    #     user = CustomUser.objects.get(email=self.request.user.email)
    #     experiences = Experience.objects.none()#filter(owner=user).values_list('id', flat=True)
    #     print(experiences)
    #     lista_corsi = get_exact_match(Course, "courses", experiences)
    #     print(lista_corsi)
    #     return lista_corsi

    def get_queryset(self):
        # TODO: fix missing degree field in admin user
        print("email: %s \n" % self.request.user.email)
        user = CustomUser.objects.get(email=self.request.user.email)
        # print("User: %s" % (dir(user)))
        # subs = User.objects.filter(subscribed_to__subscriber=request.user).values_list('id')
        # profiles = UserCommunityProfile.objects.exclude(owner__in=subs)
        # degree_id = user.degree.all().values_list('id')
        # courses = Course.objects.filter(degree__in=degree_id)
        # qs = Course.objects.all()
        # for degree in user.degree.all():
        #     qs.union(Course.objects.filter(degree=degree))
        #     print(f"Union {qs}")
        #
        #     # print("Degree: %s"%degree)
        #     # print(Course.objects.filter(degree=degree))
        # print(f"Union {qs}")
        # return Course.objects.filter(degree=user.degree)
        courses_qs = user.get_courses()
        courses = {}
        for course in courses_qs:
            courses[course] = (course.note_set.exclude(owner=user),
                               course.experience_set.exclude(owner=user))
        return courses

    # TODO: https://docs.djangoproject.com/en/3.1/topics/db/examples/
    # start from here
    def get_context_data(self, **kwargs):
        #     # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(email=self.request.user.email)

        #     courses = Course.objects.filter(degree=user.degree)
        #     # Add in a QuerySet of all the books
        context['notes'] = Note.objects.exclude(owner=user)
        context['exps'] = Experience.objects.exclude(owner=user)
        return context


class PurchasedNotesList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'content/purchased_list.html'

    def get_queryset(self):
        user = CustomUser.objects.get(email=self.request.user.email)
        return user.purchased_notes.all()


@login_required
@require_POST
def buy_note(request):
    print("ciao")
    user = CustomUser.objects.get(email=request.user.email)
    id = request.POST.get('id', None)
    to_buy = Note.objects.filter(id=id).get()
    user.purchased_notes.add(to_buy)
    print(user.purchased_notes.all())
    # ctx = {'valid': valid, 'message': message}
    return HttpResponse(json.dumps({}), content_type='application/json')
