from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views import View
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Answer, Category, Quiz, Question


def HomePageView(request):
    if request.method == "GET":
        return render(request, 'simple_quiz/home.html')


class QuizListView(ListView):
    model = Quiz

    def get_queryset(self):
        if self.request.user.is_authenticated():
            queryset = Quiz.objects.filter(is_published=True).prefetch_related('quizzes')
        else:
            queryset = Quiz.objects.filter(Q(is_published=True) & Q(allow_anonymous=True)).prefetch_related('quizzes')
        return queryset


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'slug'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = self.object.questions.first().id

        if not self.object.is_published:
            raise PermissionDenied

        if (not request.user.is_authenticated()) and (not self.object.allow_anonymous):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)

        request.session['quiz_id'] = self.object.slug
        request.session['used_questions'] = []

        # url to start quiz with first question
        context['question'] = reverse('question', kwargs={'id': str(id)})
        response = self.render_to_response(context)
        response.set_signed_cookie('answer_count', 0)
        return response

    def post(self, request, *args, **kwargs):
        points = 0
        _ids = [(lambda key: int(key.split('_')[1]) if key.startswith('answer_') else None)(key) for key in request.POST]
        # list of answers id's
        ids = [id for id in _ids if id is not None]

        quiz_id = request.session.get('quiz_id', None)
        slug = kwargs.get('slug', None)

        # check if started quiz same as currently running
        if quiz_id != slug:
            return HttpResponseRedirect(reverse('quiz_start_page', kwargs={'slug': slug}))

        # current question
        question_id = kwargs.get('question', None)
        question = Question.objects.get(id=question_id)

        # check answers; Only correct answers give one point
        valid = question.answers.filter(is_valid=True).exclude(id__in=ids).exists()
        invalid = question.answers.filter(Q(is_valid=False) & Q(id__in=ids)).exists()
        if (not valid) and (not invalid):
            points = 1

        # trick to append into session list
        exclude_questions = request.session['used_questions']
        exclude_questions.append(question_id)
        request.session['used_questions'] = exclude_questions


        self.object = self.get_object()
        questions = self.object.questions.all().exclude(id__in=exclude_questions).exists()

        # get current score
        score = request.get_signed_cookie('answer_count')

        # no more questions
        if not questions:
            final_score = int(score) + points
            questions_count = self.object.questions.all().count()
            return render(request,
                          template_name='simple_quiz/result_page.html',
                          context={
                              'quiz': self.object,
                              'score': final_score,
                              'total': questions_count
                          })

        # get next question
        next_question_id = self.object.questions.all().exclude(id__in=exclude_questions).first().id

        response = HttpResponseRedirect(reverse('question', kwargs={'id': next_question_id}))
        response.set_signed_cookie('answer_count', int(score) + points)
        return response



class QuestionView(View):

    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(
            Question,
            id=self.kwargs['id']
        )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.question
        answers = queryset.answers.all()

        return render(request, 'simple_quiz/question.html', context={'question': queryset, 'answers': answers})


class CategoriesListView(ListView):
    model = Category


class CategoryDetailView(ListView):
    model = Category
    template_name = 'simple_quiz/view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['slug']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = self.category
        if self.request.user.is_authenticated:
            context['quizzes'] = self.category.quizzes.filter(is_published=True)
        else:
            context['quizzes'] = self.category.quizzes.filter(Q(is_published=True) & Q(allow_anonymous=True))
        return context

    def get_queryset(self):
        queryset = self.category
        return queryset
