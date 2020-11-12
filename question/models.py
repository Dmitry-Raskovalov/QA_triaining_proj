from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from question.utils import unique_slug_generator


class Author(models.Model):
    nickname = models.CharField("Отображаемое имя", max_length=100, unique=True)
    name = models.CharField("Имя Фамилия", max_length=100, blank=True)
    reg_time = models.DateField("Дата регистрации", auto_now_add=True)
    visited_time = models.DateTimeField("Время последнего посещения", auto_now_add=True)
    # number_questions = models.PositiveSmallIntegerField("количество вопросов", default=0)
    # number_answers = models.PositiveSmallIntegerField("количество ответов", default=0)
    # number_comments = models.PositiveIntegerField("количество комментариев", default=0)
    avatar = models.ImageField("Аватарка", upload_to="avatars/", blank=True)
    mail = models.EmailField("E-mail", unique=True)
    info = models.TextField("Информация", blank=True)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


# DELETED_AUTHOR = Author.objects.get_or_create(
#     nickname="Deleted_author",
#     mail="del_author@del.com",
#     info="Учетаная запись автора удалена",
#     url="deleted_author"
# )


class MessageInfo(models.Model):
    content = models.TextField("Текст")
    author = models.ForeignKey(Author, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    #TODO: разобраться как устанавливать дефолтную модель default=Author.objects.get(nickname="Deleted_author"))
    creation_time = models.DateTimeField("Время создания", auto_now_add=True)
    change_time = models.DateTimeField("Время изменения", auto_now_add=True)
    rating = models.PositiveIntegerField("Рейтинг", default=0)
    draft = models.BooleanField("Черновик", default=False)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField("Имя", max_length=40)
    description = models.TextField("Описание", blank=True)
    number_questions = models.PositiveIntegerField("количество вопросов", blank=True, default=0)
    url = models.SlugField(blank=True, max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag", kwargs={"slug": self.url})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"


class Comment(MessageInfo):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    votes = models.ManyToManyField(Author, verbose_name="Голоса", related_name="comment_vote", blank=True)

    def __str__(self):
        return f"comment {self.content_object} - {self.author}"
        # TODO: изменить отображение названия коммента в админке

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Question(MessageInfo):
    header = models.CharField("Заголовок", max_length=500)
    content = models.TextField("Текст", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги", related_name="question_tags")
    action_time = models.DateTimeField("время последнего действия", auto_now_add=True)
    views = models.PositiveIntegerField("Просмотры", blank=True, default=0)
    comments = GenericRelation(Comment)
    votes = models.ManyToManyField(Author, verbose_name="Голоса", related_name="question_vote", blank=True)
    # number_answers = models.PositiveSmallIntegerField("количество ответов", default=0)
    # correct_answer = models.BooleanField("Правильный ответ", default=False)
    #url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.header[0:30]

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk":self.pk})

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["-action_time"]


class Answer(MessageInfo):
    correct_answer = models.BooleanField("Правильный ответ", default=False)
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    comments = GenericRelation(Comment)
    votes = models.ManyToManyField(Author, verbose_name="Голоса", related_name="answer_vote", blank=True)

    def __str__(self):
        return f"{self.content[0:30]}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Synonym(models.Model):
    name = models.CharField("Имя", max_length=100)
    tag = models.ForeignKey(Tag, verbose_name="Тэг", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Синоним"
        verbose_name_plural = "Синонимы"
