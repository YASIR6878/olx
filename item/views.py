from django.shortcuts import redirect, render,get_object_or_404
from .models import Item,Category
from .forms import Sellerform,Edititemform
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def sell(request):
    if request.method == 'POST':
        form = Sellerform(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.image1= request.FILES.get('img1')
            item.image2= request.FILES.get('img2')
            item.image3= request.FILES.get('img3')

            item.created_by = request.user
            item.save()

            return redirect('index')
    else:
        form = Sellerform()

    return render(request, 'sell.html', {'form': form})


def detail(request,pk):#primary key=pk
    item=get_object_or_404(Item,pk=pk)
    releateditems=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:4]
    return render(request,'detail.html',{'item':item,'releateditems':releateditems})

@login_required
def search(request):
    if request.user.is_anonymous:
       return render(request,'login.html')
    else:
       query=request.GET.get('query','')
       categories=Category.objects.all()
       category_id=request.GET.get('category',0)
       items=Item.objects.filter(is_sold=False)
       if category_id:
           items=items.filter(category_id=category_id)
       if query:
           items=items.filter(Q(name__icontains=query) | Q(description__icontains=query))
       return render(request,'search.html',{'items':items,'category_id':int(category_id),'query':query,'categories':categories})



@login_required
def delete(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    item.delete()

    return redirect('dashboard:dash')

@login_required
def edit(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    if request.method=='POST':
        form=Edititemform(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail',pk=item.id)
    else:
        form=Edititemform(instance=item)
    return render(request,'sell.html',{'form':form})
