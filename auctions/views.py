from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.urls import reverse
from .notification import send_winner_notification 
from django.views.decorators.http import require_POST
from .models import Auction, Bid
from .forms import ImageUploadForm

# Main page
def index(request):
    # First get all auctions and resolve them
    auction_list = Auction.objects.all()
    for a in auction_list:
        a.resolve()
    # Get all active auctions, oldest first
    latest_auction_list = auction_list.filter(is_active=True).order_by('date_added')
    template = loader.get_template('auctions/index.html')
    context = {
        'title': "Active auctions",
        'auction_list': latest_auction_list,
    }
    return HttpResponse(template.render(context, request))

def auctions(request):
    # Get all auctions, newest first
    auction_list = Auction.objects.order_by('-date_added')
    for a in auction_list:
        a.resolve()
    template = loader.get_template('auctions/index.html')
    context = {
        'title': "All auctions",
        'auction_list': auction_list,
    }
    return HttpResponse(template.render(context, request))

# Details on some auction
def detail(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    auction.resolve()
    already_bid = False
    if request.user.is_authenticated:
        if auction.author == request.user:
            own_auction = True
            return render(request, 'auctions/detail.html', {'auction': auction, 'own_auction': own_auction})

        user_bid = Bid.objects.filter(bidder=request.user).filter(auction=auction).first()
        if user_bid:
            already_bid = True
            bid_amount = user_bid.amount
            return render(request, 'auctions/detail.html', {'auction': auction, 'already_bid': already_bid, 'bid_amount': bid_amount})

    return render(request, 'auctions/detail.html', {'auction': auction, 'already_bid': already_bid})
    # try:
    #     auction = Auction.objects.get(pk=auction_id)
    # except Auction.DoesNotExist:
    #     raise Http404("Auction does not exist")
    # return render(request, 'auctions/detail.html', {'auction': auction})

# def results(request, auction_id):
#     response = "You're looking at the results of auction %s."
#     return HttpResponse(response % auction_id)

# Bid on some auction
@login_required
def bid(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    auction.resolve()
    bid = Bid.objects.filter(bidder=request.user).filter(auction=auction).first()
    if not auction.is_active:
        return render(request, 'auctions/detail.html', {
            'auction': auction,
            'error_message': "The auction has expired.",
        })

    try:
        bid_amount = request.POST['amount']
        # Prevent user from entering an empty or invalid bid
        highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
        if highest_bid:
         if not bid_amount or int(bid_amount) < highest_bid.amount:
            raise(KeyError)
        else:
              if not bid_amount or int(bid_amount) < auction.min_value:
               raise(KeyError)
        if not bid:
            # Create new Bid object if it does not exist
            bid = Bid()
            bid.auction = auction
            bid.bidder = request.user
        bid.amount = bid_amount
        bid.date = datetime.now(timezone.utc)
        bid.save()
    except (KeyError):
        # Redisplay the auction details.
        return render(request, 'auctions/detail.html', {
            'auction': auction,
            'error_message': "Invalid bid amount.",
        })
    else:
        

        return redirect('auctions:index')


# Create auction
@login_required
def create(request):
    submit_button = request.POST.get('submit_button')
    if submit_button:
        try:
            title = request.POST['title']
            auction_duration = request.POST['duration']
            min_value = request.POST['min_value']
            contact= request.POST['contact']

            if not title or not min_value or not contact:
                raise(KeyError)
        except (KeyError):
            # Redisplay the create auction page with an error message.
            return render(request, 'auctions/create.html', {
                'error_message': "Please fill the required fields.",
            })
        else:
            # Create new Bid object
            auction = Auction()
            auction.author = request.user
            auction.title = title
            auction.duration=auction_duration
            auction.min_value = min_value
            auction.contact=contact
            auction.desc = request.POST['description']
            img = request.FILES.get('img')  # Use get to avoid MultiValueDictKeyError
            auction.image=img
            # auction.date_added = datetime.utcnow()
            auction.date_added = datetime.now(timezone.utc)
            auction.save()
            # return HttpResponseRedirect(reverse('auctions:detail', args=(auction.id,)))
            return redirect('auctions:my_auctions')
    else:
        return render(request, 'auctions/create.html')


@login_required
def my_auctions(request):
    # Get all auctions by user, sorted by date
    my_auctions_list = Auction.objects.all().filter(author=request.user).order_by('-date_added')
    for a in my_auctions_list:
        a.resolve()
    template = loader.get_template('auctions/my_auctions.html')
    context = {
        'my_auctions_list': my_auctions_list,
    }
    return HttpResponse(template.render(context, request))

@login_required
def my_bids(request):
    # Get all bids by user, sorted by date
    my_bids_list = Bid.objects.all().filter(bidder=request.user).order_by('-date')
    for b in my_bids_list:
        b.auction.resolve()

    template = loader.get_template('auctions/my_bids.html')
    context = {
        'my_bids_list': my_bids_list,
    }
    return HttpResponse(template.render(context, request))

