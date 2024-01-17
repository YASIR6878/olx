from django.shortcuts import get_object_or_404, redirect, render
from item.models import Item
from django.contrib.auth.decorators import login_required
from .models import Conversation
from .forms import ConversationmessageForm
@login_required
def contact(request,item_pk):
    item=get_object_or_404(Item,pk=item_pk)

    if item.created_by==request.user:
        return redirect('dashboard:index')
    conversations=Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    if conversations:
       pass 
    if request.method=='POST':
        form=ConversationmessageForm(request.POST)
        if form.is_valid():
            conversation=Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()

            return redirect('item:detail',pk=item_pk)
    else:
        form=ConversationmessageForm

    return render(request,'chat.html',{
            'form':form
        })

@login_required
def inbox(request):
     conversations=Conversation.objects.filter(members__in=[request.user.id])
     return render(request,'inbox.html',{
         'conversations':conversations
     })

@login_required
def inboxdetail(request,pk):
     conversation=Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
     if request.method=="POST":
         form=ConversationmessageForm(request.POST)
         if form.is_valid():
            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            conversation.save()
            return redirect('conversation:inboxdetail',pk=pk)
     else:
          form=ConversationmessageForm
     return render(request,'inboxdetail.html',{
         'conversation':conversation,
         'form':form
         })