from django import forms
# from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.forms import formset_factory

from question.models import Question, Tag

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MultiTag(forms.Field):
    def to_python(self, value):
        """преобразовывает строку в список тегов"""
        if not value:
            return []
        tags_str = value.split(sep=',')
        tags = map(lambda x: x.strip(), tags_str)  # в списке тэгов убирает пробелы
        tags = list(filter(None, tags))  # и удаляет пустые значения
        return tags

    def validate(self, value):
        super().validate(value)
        errors = []
        tags = value
        if len(tags) > 5:
            errors = ValidationError('Вы присвоили вопросу больше 5 меток')
        for tag in tags:
            # MaxLengthValidator(tag, value=35, message='Длина метки более 35 символов')
            if len(tag) > 35:
                errors += ValidationError(
                    'Длина метки %(tag)s более 35 символов',
                    code='invalid',
                    params={'tag': tag}
                )
        if errors:
            raise ValidationError(errors)

class QuestionForm(forms.ModelForm):
    # captcha = ReCaptchaField()
    content = forms.CharField(label='Вопрос', widget=CKEditorUploadingWidget())
    multitag = MultiTag()
    new_tags = [10,20]
    # required_css_class = "form-control"
    # error_css_class = "alert alert-danger"

    # def clean_multitag(self):
    #     # errors = {}
    #     tags = self.cleaned_data['multitag']
    #     print('claen_multitag self.new_tags=',self.new_tags)
    #     tags_cl = {'old': [], 'new': []}
    #     for tag in tags:
    #         tag = tag.strip()
    #         if not Tag.objects.filter(name=tag).exists():
    #             tags_cl['new'].append({'create': False, 'name': tag, 'description': ''})
    #         else:
    #             tags_cl['old'].append(tag)
    #     self.new_tags = tags_cl['new']
    #     new_tags_name = list(map(lambda tag: tag['name'], tags_cl['new']))
    #     new_tags_str= ', '.join(new_tags_name)  # строка с именами новых тегов
    #     err_str = {'new_tags': new_tags_str}
    #     s = {'tag': 'Метки', 'it': 'её'} if len(tags_cl['new']) == 1 else {'tag': 'Меток', 'it': 'их'}
    #     err_str.update(s)
    #     errors = ValidationError(
    #         '%(tag)s %(new_tags)s нет в нашей базе. Если вы хотите создать %(it)s отметьте чекбоксом и \
    #         напишите небольшое описание. Если вы ошиблись в написании - просто исправьте ошибку в строке \
    #         с метками',
    #         code='invalid',
    #         params=err_str
    #     )
    #     if errors:
    #         raise ValidationError(errors)
    #     print('tags_cl=',tags_cl)
    #     return tags_cl
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     print('clean self.cleaned_data', cleaned_data)
    #     # self.new_tags = cleaned_data.get('multitag')
    #     # print('clean self.new_tags=', self.new_tags)


    class Meta:
        model = Question
        fields = ('header', 'content', 'multitag')


class TagForm (forms.ModelForm):
    create_tag = forms.BooleanField(required=False)


    class Meta:
        model = Tag
        fields = ('create_tag', 'name', 'description')