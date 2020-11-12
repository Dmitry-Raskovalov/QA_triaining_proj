from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import SingleObjectMixin

from question.forms import QuestionForm, TagForm
from question.models import Question, Tag
from question.utils import unique_slug_generator


class TagsMixin(ContextMixin):
    """
    Добавляет в контекст теги отсортированные по количеству записей
    для отображения в правой колонке
    """
    def get_context_data(self, **kwargs):
        context = {}
        if Tag.objects.all().exists():
            tags = Tag.objects.order_by('number_questions')[0:50]
            context['popular_tags'] = tags
            context.update(kwargs)
        return super().get_context_data(**context)

class IndexView(TagsMixin, ListView):
    """
    Главная страница
    """
    queryset = Question.objects.filter(draft=False)
    context_object_name = 'newest_question'
    paginate_by = 2
    template_name = 'question/index.html'


class AskQuestionView(FormView):
    """
    Форма "задать вопрос"
    """
    template_name = 'question/ask_question.html'
    # form_class = QuestionForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = QuestionForm(initial=self.initial)
        formset = None
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        print('form.new_tags', form.new_tags)
        TagFormSet = formset_factory(TagForm)
        formset = TagFormSet(initial=form.new_tags)
        if form.is_valid():
            question = form.save(commit=False)
            # print(form.cleaned_data['multitag'])
            self.add_question_tags(question, form.cleaned_data['multitag'])
            question = form.save()
            # for tag in form.cleaned_data['multitag']:
            #     t = Tag.objects.get(name=tag)
            #     question.tags.add(t)
            # self.add_question_tags(question, form.cleaned_data['multitag'])
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form, 'formset': formset})

    # def formset_data(self, **newtags):
    #     data = []
    #     for tag in newtags:
    #         data += {'create': tag['create'], 'name': tag['name'], 'description': tag['description']}
    #     return data


    def add_question_tags(self, question, **tags):
        # Добавляет метки к вопросу
        print('tags=', tags)
        for tag in tags['old']:
            t = Tag.objects.get(name=tag)
            question.tags.add(t)
        for tag in tags['new']:
            t = Tag(name=tag, description='', slug=unique_slug_generator(tag, Tag))
            t.save()
        return question




    # def post(self):
    #     form = QuestionForm(request.POST)
    #     # if form.is_valid():
    #     #     form = form.save(commit=False)
    #     #     if request.POST.get("parent", None):
    #     #         form.parent_id = int(request.POST.get("parent"))
    #     #     form.movie = movie
    #     #     form.save()
    #     return redirect('')
    #
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     # form.send_email()
    #     return super().form_valid(form)


# class AddQuestion(View):
#     def post(self):
#         form = QuestionForm(request.POST)
#         # if form.is_valid():
#         #     form = form.save(commit=False)
#         #     if request.POST.get("parent", None):
#         #         form.parent_id = int(request.POST.get("parent"))
#         #     form.movie = movie
#         #     form.save()
#         return redirect('')


class QuestionView(TagsMixin, DetailView):
    """
    Страница вопроса
    """
    model = Question
    queryset = Question.objects.filter(draft=False)


class TagView(TagsMixin, SingleObjectMixin, ListView):
    """
    Страница одного тэга, со списком вопросов с этим тэгом
    """
    template_name = 'question/tag.html'
    paginate_by = 1
    slug_field = 'url'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.object
        return context

    def get_queryset(self):
        return self.object.question_tags.all()


class TagIndexView(ListView):
    """
    Страница со списком тэгов
    """
    model = Tag
    template_name = 'question/tags_index.html'
    paginate_by = 6

class SearchView(TagsMixin, ListView):
    """
    Страница поиска
    """
    model = Question
    template_name = 'search_page.html'
    paginate_by = 1

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Question.objects.filter(Q(draft=False) & Q(header__icontains=query) | Q(content__icontains=query))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get("q")
        context["q_str"] = f'q={self.request.GET.get("q")}&'
        context['number_of_questions'] = self.get_queryset().count()
        return context
