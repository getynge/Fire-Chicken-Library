def compute_tag_name(partial_name: str):
    if has_prefix(partial_name):
        return partial_name
    else:
        return 'user.' + partial_name
    
def has_prefix(text: str):
    return text.find('.') > 0

def deactivate_tags_in_context(context):
    context.tags = []

def make_tag_only_active_tag_in_context(tag_name: str, context):
    context.tags = [tag_name]

def compute_name_dot_index(tag_name: str) -> int:
    return tag_name.find('.')

def compute_postfix(tag_name: str) -> str:
    dot_index = compute_name_dot_index(tag_name)
    return tag_name[dot_index + 1:]

def compute_prefix(tag_name: str):
    dot_index = compute_name_dot_index(tag_name)
    return tag_name[:dot_index]
