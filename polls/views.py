from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Choice

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_questions': latest_questions})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Se nenhuma opção foi selecionada, mostrar erro
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Você precisa selecionar uma opção.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', question_id=question.id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    total_votes = sum(choice.votes for choice in question.choice_set.all())
    
    choices_with_percentages = []
    for choice in question.choice_set.all():
        # Agora multiplicamos por 100 para garantir a porcentagem correta
        percentage = (choice.votes / total_votes) * 100 if total_votes > 0 else 0
        choices_with_percentages.append({
            'choice_text': choice.choice_text,
            'votes': choice.votes,
            'percentage': round(percentage, 2),  # Usando round para limitar a 2 casas decimais
        })
    
    return render(request, 'polls/results.html', {
        'question': question,
        'choices': choices_with_percentages,
        'total_votes': total_votes,
    })

