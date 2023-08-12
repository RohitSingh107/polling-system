from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Poll
from .forms import PollForm, ChoiceForm

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))



def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save()
            # return redirect('polls:index')  # Redirect to poll list
            return redirect('polls:detail', poll_id=poll.id)  # Redirect to poll detail
    else:
        form = PollForm()
    return render(request, 'polls/create_poll.html', {'form': form})


def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.poll = poll
            choice.save()
            return redirect('polls:detail', poll_id=poll.id)  # Redirect to poll detail
    else:
        form = ChoiceForm()
    return render(request, 'polls/add_choice.html', {'form': form, 'poll': poll})
