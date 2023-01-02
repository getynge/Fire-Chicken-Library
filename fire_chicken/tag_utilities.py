def compute_tag_name(partial_name: str):
    if has_prefix(partial_name):
        return partial_name
    else:
        return 'user.' + partial_name
    
def has_prefix(text: str):
    return text.find('.') > 0
