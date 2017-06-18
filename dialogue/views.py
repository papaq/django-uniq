from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

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

    if request.user not in dialogue.participants.all():
        return redirect('dialogue:dialogue_list')

    form = MessageForm(request.POST or None)

    if form.is_valid():
        text = form.cleaned_data['message']
        message = Message(sender=request.user, text=text, dialogue=dialogue)
        message.save()

    messages = Message.objects.filter(dialogue=dialogue_pk).order_by('date')
    second_participant = None

    for participant in dialogue.participants.all():
        if participant.pk is not request.user.pk:
            second_participant = participant

    context = {
        'second_participant': second_participant,
        'messages': messages,
        'form': form,

    }

    return render(request, "dialogue/dialogue_chat.html", context)


def get_messages(request):
    dialogue_pk = request.GET.get('dialogue', None)

    dialogue = get_object_or_404(Dialogue, pk=dialogue_pk)
    if request.user not in dialogue.participants.all():
        raise Http404("You are not suggested to see this")

    messages_number = request.GET.get('messages_number', None)
    messages = Message.objects.filter(dialogue=dialogue_pk).order_by('-date')
    new_messages_number = messages.count()-int(messages_number)

    new_messages = messages[:new_messages_number]
    second_participant = None

    for participant in dialogue.participants.all():
        if participant.pk is not request.user.pk:
            second_participant = participant

    template = 'dialogue/messages.html'
    context = {
        'second_participant': second_participant,
        'messages': new_messages,
    }

    return render(request, template, context)