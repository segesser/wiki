from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect




class ContactForm(forms.Form):
    css = {"all": ("encyclopedia/formstyles.css",)}
    yourname = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(required=False, label='Your Email Address')
    subject = forms.CharField(max_length=100, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")


# def contact(request):
#     form1 = ContactForm(request.POST)
#     return render(request, "encyclopedia/contact.html", {
#         "form": form1
# })


def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 
        'encyclopedia/contact.html', 
        {'form': form, 'submitted': submitted}
        )
