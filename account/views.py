from django.shortcuts import reverse, redirect, render
from django.utils.decorators import method_decorator
from django.core.urlresolvers import resolve, reverse_lazy
from django.http import Http404
from django.contrib.auth.views import password_change, login
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .forms import AddressForm, CreditCardForm
from .models import Address, CreditCard
from . import login_required

# used in logout view for redirection to 'index'
password_change.login_required = True

@login_required
def index(request):
    address_count = request.user.addresses.count()
    card_count = request.user.cards.count()
    order_count = request.user.orders.count()
    review_count = request.user.reviews.count()
    links = []
    if address_count:
        links.append({
            'name': 'Addresses',
            'href': reverse('account:addresses'),
        })
    else:
        links.append({
            'name': 'Add Address',
            'href': reverse('account:add_address'),
        })

    if card_count:
        links.append({
            'name': 'Cards',
            'href': reverse('account:cards'),
        })
    else:
        links.append({
            'name': 'Add Card',
            'href': reverse('account:add_card'),
        })

    if order_count:
        links.append({
            'name': 'Orders',
            'href': reverse('account:orders'),
        })

    if review_count:
        links.append({
            'name': 'Reviews',
            'href': reverse('account:reviews'),
        })

    return render(request, 'account/index.html', {'links': links})

def logout(request):
    from django.contrib.auth import logout as auth_logout
    from commerce import get_cart

    cart = get_cart(request.session)
    auth_logout(request)
    request.session['cart'] = cart
    url = request.GET.get('next', reverse('index'))

    view = resolve(url).func
    if getattr(view, 'login_required', False):
        url = reverse('index')

    return redirect(url)

class Register(CreateView):
    template_name = 'account/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            try:
                Address.objects.create(user=request.user, **form.cleaned_data)
                return redirect(reverse('account:addresses'))
            except IntegrityError:
                form.add_error(
                    None,
                    ValidationError('This address already exists.')
                )
    else:
        form = AddressForm()

    return render(request, 'account/add_address.html', {'form': form})

@login_required
def edit_address(request, pk):
    pass

@login_required
def delete_address(request, pk):
    pass

@login_required
def add_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            del form.cleaned_data['card_number']
            # encrypt card number
            try:
                CreditCard.objects.create(
                    user=request.user,
                    card_number=card_number,
                    **form.cleaned_data
                )

                return redirect(reverse('account:cards'))
            except IntegrityError:
                form.add_error(
                    None,
                    ValidationError('This credit card already exists.')
                )
    else:
        form = CreditCardForm()

    return render(request, 'account/add_card.html', {'form': form})

@login_required
def edit_card(request, pk):
    pass

@login_required
def delete_card(request, pk):
    pass

@login_required
def edit_review(request, pk):
    pass

@login_required
def delete_review(request, pk):
    pass

class AddressList(ListView):
    template_name = 'account/addresses.html'

    def get_queryset(self):
        query = self.request.user.addresses.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CardList(ListView):
    template_name = 'account/cards.html'

    def get_queryset(self):
        query = self.request.user.cards.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class OrderList(ListView):
    template_name = 'account/orders.html'

    def get_queryset(self):
        query = self.request.user.orders.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class OrderDetails(DetailView):
    template_name = 'account/order.html'

    def get_queryset(self):
        query = self.request.user.orders.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ReviewList(ListView):
    template_name = 'account/reviews.html'

    def get_queryset(self):
        query = self.request.user.reviews.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
