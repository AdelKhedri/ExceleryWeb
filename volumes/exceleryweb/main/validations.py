from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size = 1024 * 1024 * 50
    print(file.size)
    if file.size > max_size:
        raise ValidationError(f"File size must not more than {max_size}.")