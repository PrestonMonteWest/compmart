from django.shortcuts import reverse, redirect, render
from django.utils.decorators import method_decorator
from django.urls import resolve, reverse_lazy
from django.http import Http404
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.views import generic
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from . import forms
from .models import Address, CreditCard
from . import login_required

import logging


# used in logout view for redirection to 'index'
PasswordChangeView.as_view().login_required = True

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

    name = 'next'
    url = request.GET.get(name, None)

    if url is None:
        logger = logging.getLogger(__name__)
        logger.warning('Query parameter "{}" was not set!'.format(name))
        url = reverse('index')

    return redirect(url)


class Register(generic.CreateView):
    template_name = 'account/register.html'
    form_class = forms.MyUserCreationForm
    success_url = reverse_lazy('index')


@login_required
def add_address(request):
    form = forms.AddressForm(request.POST or None)
    if form.is_valid():
        try:
            Address.objects.create(user=request.user, **form.cleaned_data)
            if 'next' in request.GET:
                return redirect(request.GET['next'])

            return redirect(reverse('account:addresses'))
        except IntegrityError:
            form.add_error(
                None,
                ValidationError('This address already exists.')
            )

    return render(request, 'account/add_address.html', {'form': form})

@login_required
def edit_address(request, pk):
    pass

class DeleteAddress(generic.DeleteView):
    template_name = 'account/delete_address.html'

    def get_queryset(self):
        return self.request.user.addresses.all()

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        address_count = request.user.addresses.count()

        if address_count:
            url = reverse('account:addresses')
        else:
            url = reverse('account:index')

        return redirect(url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def add_card(request):
    form = forms.CreditCardForm(request.POST or None)
    if form.is_valid():
        try:
            CreditCard.objects.create(user=request.user, **form.cleaned_data)
            if 'next' in request.GET:
                return redirect(request.GET['next'])

            return redirect(reverse('account:cards'))
        except IntegrityError:
            form.add_error(
                None,
                ValidationError('This credit card already exists.')
            )

    return render(request, 'account/add_card.html', {'form': form})

@login_required
def edit_card(request, pk):
    pass

class DeleteCard(generic.DeleteView):
    template_name = 'account/delete_card.html'

    def get_queryset(self):
        return self.request.user.cards.all()

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        card_count = request.user.cards.count()

        if card_count:
            url = reverse('account:cards')
        else:
            url = reverse('account:index')

        return redirect(url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def edit_review(request, pk):
    pass

class DeleteReview(generic.DeleteView):
    template_name = 'account/delete_review.html'

    def get_queryset(self):
        return self.request.user.reviews.all()

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        review_count = request.user.reviews.count()

        if review_count:
            url = reverse('account:reviews')
        else:
            url = reverse('account:index')

        return redirect(url)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressList(generic.ListView):
    template_name = 'account/addresses.html'

    def get_queryset(self):
        query = self.request.user.addresses.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CardList(generic.ListView):
    template_name = 'account/cards.html'

    def get_queryset(self):
        query = self.request.user.cards.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class OrderList(generic.ListView):
    template_name = 'account/orders.html'

    def get_queryset(self):
        query = self.request.user.orders.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class OrderDetails(generic.DetailView):
    template_name = 'account/order.html'

    def get_queryset(self):
        query = self.request.user.orders.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ReviewList(generic.ListView):
    template_name = 'account/reviews.html'

    def get_queryset(self):
        query = self.request.user.reviews.all()
        if not query:
            raise Http404()

        return query

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
