import re


def get_non_matching_fields(regexes, fields):
    non_matching_fields = []

    for i, (regex, field) in enumerate(zip(regexes, fields)):
        if not re.match(regex, field['value']):
            non_matching_fields.append(i)

    return non_matching_fields
