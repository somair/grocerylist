# stores/views.py
from __future__ import absolute_import

from django.views import generic
from django.contrib import messages

from items.forms import ItemCreateForm
from items.models import Item

from isles.models import Isle

from lists.models import List
from lists.forms import ListForm

from .forms import StoreForm
from .models import Store


class StoreIndex(generic.TemplateView):
    """ The default view for /s/ ; a list of stores """
    form_class, model = StoreForm, Store
    template_name = 'stores/index.html'

    def get_context_data(self, **kwargs):
        context = super(StoreIndex, self).get_context_data(**kwargs)
        context['stores'] = Store.objects.all().values('slug', 'name')
        return context


class StoreDetailView(generic.DetailView):
    """ View a Store
    And show a ton of dynamic data
    """
    form_class, model = StoreForm, Store
    template_name = 'stores/StoreDetailView.html'

    def get_context_data(self, **kwargs):
        """
            Ugg....
        """
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        #
        # Items that belong to this store.
        local_items = Item.objects.filter(store=self.object.id).order_by('isle')
        if local_items:
            context['Items'] = local_items
            context['ListForm'] = ListForm()
            context['ListForm'].fields['items'].queryset = local_items
            
        #
        # Isles that belong to this store
        local_isles = Isle.objects.filter(store=self.object.id)
        if local_isles:
            context['isles'] = local_isles
            context['ItemCreateForm'] = ItemCreateForm()
            context['ItemCreateForm'].fields['isle'].queryset = local_isles
            context['ItemCreateForm'].fields['isle'].initial = local_isles[0]
        #
        # My Grocery Lists that reference this store, newest first
        context['related_lists'] = List.objects.filter(store=self.object.id).order_by('-pk')
        return context


class StoreUpdateView(generic.UpdateView):
    """Edit a Store"""
    form_class, model = StoreForm, Store
    template_name = 'stores/StoreUpdateView.html'

    def form_valid(self, form):
        messages.success(self.request, 'Changes saved!')
        return super(StoreUpdateView, self).form_valid(form)


class StoreCreateView(generic.CreateView):
    """Make a new Store"""
    form_class, model = StoreForm, Store
    template_name = 'stores/StoreCreateView.html'

    def form_valid(self, form):
        messages.success(self.request, 'Store "%s" added!' % form.cleaned_data['name'] )
        return super(StoreCreateView, self).form_valid(form)
