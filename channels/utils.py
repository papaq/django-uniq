def combine_sets(**model_sets):
    if not model_sets:
        return None

    combined_set = None

    for _, model_set in model_sets.items():
        if not combined_set and model_set:
            combined_set = model_set
        if model_set:
            combined_set = combined_set | model_set

    return combined_set


def count_recent_posts(posts_set, user):
    recent = len(posts_set.exclude(read=user))

    return recent
