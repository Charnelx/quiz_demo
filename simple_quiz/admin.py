from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Category, Quiz, Question, Answer
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
import nested_admin

from django.utils.html import mark_safe


def build_fields_links(queryset, attr, no_margin=False):
    links = []
    for item in queryset:
        instance = getattr(item, attr, '')
        url = reverse("admin:%s_%s_change" % (item._meta.app_label, item._meta.model_name),
                                   args=(item.id,))
        links.append('<li style="list-style: none;"><a href="{0}">{1}</a></li>'.format(url, instance))
    link = '<ul {margin}>{items}</ul>'.format(items=''.join(links),
                                              margin='style="margin-left: 0px;padding-left: 0px;"'
                                              if no_margin else 'style="margin-top: 0px; margin-left: 0px;"')
    return mark_safe(link)


class AnswerInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        count_valid = 0
        for form in self.forms:
            if not form.is_valid():
                return  # other errors exist
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data['is_valid']:
                    count_valid += 1 # should run at least one's (question should contain valid answer(s))

        if count_valid == 0:
            raise ValidationError('You should to specify at least one valid answer!')


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 2
    formset = AnswerInlineFormset

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


class QuizAdminForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = []
        prepopulated_fields = {"slug": ("title",)}

    quizzes = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Category",
        widget=FilteredSelectMultiple(
            verbose_name="Categories",
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['quizzes'].initial = \
                self.instance.quizzes.all()

    def save(self, commit=True):
        quiz = super().save(commit=False)
        quiz.save()
        quiz.quizzes = self.cleaned_data['quizzes']
        self.save_m2m()
        return quiz


class CategoryAdminForm(forms.ModelForm):
    """
    Category admin form.
    Related quizzes filtered by category name
    """

    class Meta:
        model = Category
        exclude = []
        prepopulated_fields = {"slug": ("name",)}
        fields = ('name', 'slug')


class QuizAdmin(nested_admin.NestedModelAdmin):
    class Media:
        css = {"all": ("simple_quiz/static/css/django_admin_extra.css",)}

    form = QuizAdminForm

    list_display = ('creation_date', 'title', '_categories', 'allow_anonymous', 'is_published',)
    list_filter = ('quizzes__name', 'allow_anonymous', 'allow_anonymous',)
    search_fields = ('description', 'category', )
    readonly_fields = ('_questions',)
    inlines = [QuestionInline]

    def _categories(self, obj):
        """
        Return comma separated string with list of quiz categories
        :param obj: model_instance
        :return: string
        """
        return obj.get_category_string()

    def _questions(self, obj):
        """
        Return read-only questions related to this Quiz
        :param obj: model_instance
        :return: string
        """
        queryset = Question.objects.filter(quiz=obj.id)
        return build_fields_links(queryset, 'question_text')


class CategoryAdmin(nested_admin.NestedModelAdmin):
    form = CategoryAdminForm

    readonly_fields = ('_quizzes',)
    search_fields = ('category', )

    def _quizzes(self, obj):
        queryset = Quiz.objects.filter(quizzes__id=obj.id)
        return build_fields_links(queryset, 'title')


class QuestionAdmin(nested_admin.NestedModelAdmin):
    class Media:
        css = {"all": ("simple_quiz/static/css/django_admin_extra.css",)}

    fields = ('quiz', 'question_text',)
    search_fields = ('question_text',)
    list_display = ('question_text', 'quizzes')
    inlines = [AnswerInline]


    def quizzes(self, obj):
        queryset = Quiz.objects.filter(questions__id=obj.id)
        return build_fields_links(queryset, 'title', no_margin=True)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)