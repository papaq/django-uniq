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


def count_new_messages(messages_set, user):
    new = 0
    for message in messages_set:
        if not message.read.all().filter(pk=user.pk):
            new += 1

    return new
