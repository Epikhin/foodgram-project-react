from django.core.exceptions import ValidationError


def validate_color_length(value):
    if not (len(value) == 7 and value.startswith('#')):
        raise ValidationError(
            'Цвет должен быть в формате "#RRGGBB" и иметь длину 7 символов.')
