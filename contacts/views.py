from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact, ContactGroup
from .forms import ContactForm


@login_required
def contact_list(request):
    contacts = Contact.objects.filter(owner=request.user)
    groups = ContactGroup.objects.filter(owner=request.user)
    group_id = request.GET.get('group')
    if group_id:
        contacts = contacts.filter(group_id=group_id)
    return render(request, 'contacts/list.html', {'contacts': contacts, 'groups': groups})


@login_required
def contact_create(request):
    form = ContactForm(
        request.POST or None,
        request.FILES or None
    )

    # محدود کردن گروه‌ها به گروه‌های متعلق به کاربر
    form.fields['group'].queryset = ContactGroup.objects.filter(
        owner=request.user
    )

    if request.method == 'POST' and form.is_valid():
        contact = form.save(commit=False)
        contact.owner = request.user
        contact.save()

        return redirect('contacts:list')

    return render(request, 'contacts/form.html', {
        'form': form
    })

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    return render(request, 'contacts/detail.html', {'contact': contact})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(
        Contact,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        contact.delete()

    return redirect('contacts:list')