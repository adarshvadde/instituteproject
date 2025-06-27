from django import template
register = template.Library()

from ..views import encode_uuid_to_base64

@register.filter
def split(dicts,value):
    return dicts.split(value)

@register.filter
def get_id(value):
    return encode_uuid_to_base64(value)



@register.filter
def get_item(dictionary, key):
    """
    Retrieves an item from a dictionary-like object (like a Django form) using a key.
    Useful for dynamically accessing form fields.
    """
    try:
        return dictionary[key]
    except KeyError:
        # Handle cases where the key might not exist (e.g., if a student has no corresponding field)
        return None
    





@register.filter(name='get_item_id')
def get_item_id(form, application_id):
    """
    Allows accessing a specific form field by constructing its name based on application_id.
    Expected field name format: 'student_{application_id}'
    Usage in template: {{ form|get_item_id:student_application.id }}
    """
    field_name = f'student_{application_id}'
    return form[field_name]

sets = set()
@register.filter
def get_item_set( ): 
    """
    Returns the value of the key in the dictionary if it exists, otherwise returns an empty list.
    """
    return sets
@register.filter
def add_to_list(original_list, value):
    """Returns a new list with value added (original list remains unchanged)."""
    if type(original_list) is not set:
        original_list = sets
        print(original_list)
    sets.add(value)
    return sets

@register.filter
def startwith(value, arg):
    """
    Returns True if the value starts with the specified argument, otherwise returns False.
    """
    return 'status' + str(arg)