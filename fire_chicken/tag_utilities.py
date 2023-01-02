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
