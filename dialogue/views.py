from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from dialogue.forms import MessageForm
from dialogue.models import Dialogue, Message


@login_required
def dialogue_list(request):
    user = request.user
    dialogues = Dialogue.objects.filter(participants__pk=user.pk).order_by('-fresh_message_date')

    context = {
        'dialogues': dialogues,
        'this_user': user,
    }

    return render(request, 'dialogue/dialogue_list.html', context)


@login_required
def dialogue_chat(request, dialogue_pk):
    dialogue = get_object_or_404(Dialogue, pk=dialogue_pk)
    form = MessageForm(request.POST or None)

    print(form.is_valid())

    if form.is_valid():
        text = form.cleaned_data['message']
        message = Message(sender=request.user, text=text, dialogue=dialogue)
        message.save()

    messages = Message.objects.filter(dialogue=dialogue_pk).order_by('date')
    second_participant = None

    for participant in dialogue.participants.all():
        if participant is not request.user:
            second_participant = participant

    context = {
        'participant': second_participant,
        'messages': messages,
        'form': form,

    }

    return render(request, "dialogue/dialogue_chat.html", context)
