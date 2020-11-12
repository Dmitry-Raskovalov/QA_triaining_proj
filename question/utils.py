from django.utils.text import slugify
import random, string

def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a url field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(name)
    class_inst = instance.__class__
    qs_exists = class_inst.objects.filter(url=slug).exists()
    if qs_exists:
        new_slug = '{slug}-{randstr}'.format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
