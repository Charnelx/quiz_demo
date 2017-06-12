from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Quiz(models.Model):
    """
    Quiz
    """
    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Title',
        help_text='<br />Try to fit in 256 characters')
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        help_text="Quiz description")
    slug = models.SlugField(unique=True, blank=True, help_text='<br />Leave blank for auto-generated slug.')
    preserve_order = models.BooleanField(default=True)
    allow_anonymous = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    creation_date = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    def get_absolute_url(self):
        return reverse('quiz', args=(self.slug,))

    def get_category(self):
        return self.quizzes.all()

    def get_category_string(self):
        """
        Get category(ies) of Quiz instance.

        return: string
        """
        return ', '.join([cat.name for cat in self.quizzes.all()])

    def get_questions(self):
        return self.questions.all()


class Question(models.Model):
    """
    Questions related to quiz
    """
    question_text = models.TextField(verbose_name='Question\'s text')
    quiz = models.ForeignKey(Quiz, related_name='questions')

    def __str__(self):
        return "{content}".format(content=self.question_text)


class Answer(models.Model):
    """
    Answer's Model, which is used as the answer in Question Model
    """
    text = models.TextField(verbose_name='Answer\'s text')
    is_valid = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'question'

    def __str__(self):
        return self.text


class Category(models.Model):
    """
    Quiz category
    """
    name = models.CharField(
        db_index=True,
        max_length=128,
        verbose_name='Category name',
        unique=True,
        help_text='<br /> Try to fit in 128 characters',
        default='Misc')
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text='<br />Leave blank for auto-generated slug.')
    quizzes = models.ManyToManyField(
        to=Quiz,
        related_name='quizzes',
        help_text='<br /> Quizzes related to this group.')


    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name


    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()


    def get_absolute_url(self):
        return reverse('category_detail', args=(self.slug,))
