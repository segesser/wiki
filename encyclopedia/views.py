from logging import PlaceHolder
from re import X
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2
from markdown2 import Markdown

class NewWikiEntry(forms.Form):
    name = forms.CharField(label="New Entry Name", max_length=100)
    content = forms.CharField(label="New Entry Text", widget=forms.Textarea)


class EditWikiEntry(forms.Form):
    name = forms.CharField(label="Entry Name", required=False, max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    content = forms.CharField(label="Edit Entry Text", required=False, widget=forms.Textarea)


class NewWikiSearch(forms.Form):
    searchtext = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Search'}))

def entry(request, entry_name):
    if util.get_entry(entry_name) is None:
        return render(request, "encyclopedia/entry.html", {
            "title": "There is no such Entry: " + entry_name,
            "content": "",
            "form1": NewWikiSearch(request.GET)
        })
    
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "title": entry_name,
        #"content": util.get_entry(entry_name), ###  Markdown here!!!  ###
        "content": markdowner.convert(util.get_entry(entry_name)), #Markdown here!!!
        "form1": NewWikiSearch(request.GET)
})

def edit(request, entry_name):
    if request.method == "POST":
        form2 = EditWikiEntry(request.POST)
        if form2.is_valid():
            newcontent = form2.cleaned_data["content"]
            util.save_entry(entry_name, newcontent)
            return render(request, "encyclopedia/entry.html", {
                    "title": entry_name,
                    "content": markdown2.markdown(util.get_entry(entry_name)),
                    "form1": NewWikiSearch(request.GET)
                })
    return render(request, "encyclopedia/edit.html", {
        "title": entry_name,
        "form2": EditWikiEntry(initial={'name': entry_name, 'content': util.get_entry(entry_name)}),
        "form1": NewWikiSearch(request.GET)
    })


def new(request):
    if request.method == "POST":
        form = NewWikiEntry(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            if name in util.list_entries():
                # change HTML -> ErrorMessage
                return render(request, "encyclopedia/index.html", { ## todo
                    "title": "The Entry <"+name+"> already exists!",
                    "entries": "",
                    "form1": NewWikiSearch(request.GET)
                })
            util.save_entry(name, content)
            return render(request, "encyclopedia/entry.html", {
                "title": name,
                "content": content,
                "form1": NewWikiSearch(request.GET)
            })
        else:
            return render(request, "wiki/new.html", {
                "form": form,
                "form1": NewWikiSearch(request.GET)
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewWikiEntry(),
        "form1": NewWikiSearch(request.GET)
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries(),
        "form1": NewWikiSearch(request.GET)
    })



def randomentry(request):
    entries = util.list_entries()
    number = random.randint(1,len(entries))
    entry_name = entries[number-1]
    return render(request, "encyclopedia/entry.html", {
        "title": entry_name,
        "content": markdown2.markdown(util.get_entry(entry_name)),
        "form1": NewWikiSearch(request.GET)
})


def search(request):
    form1 = NewWikiSearch(request.GET)
    if form1.is_valid():
        searchtext = form1.cleaned_data["searchtext"]
        entries = util.list_entries()
        #CAPITALIZE THE SEARCHTEXT AND ENTRIES???
        if searchtext in entries:  #es gibt den searchtext --> öffne entry mit content
            return render(request, "encyclopedia/entry.html", {
                "title": searchtext,
                "content": util.get_entry(searchtext),
                "form1": form1
            })
        substrings = list()
        for entry in entries:
            if searchtext in entry:
                substrings.append(entry)
        if not substrings:
            print(111)
            return render(request, "encyclopedia/entry.html", {
                "title": "No Matching Search Results",
                "content": "Try searching for something different!",
                "form1": form1
            })
        return render(request, "encyclopedia/index.html", {
            "title": "Your Search was a substring of the these Entries:",
            "entries": substrings,
            "form1": form1
        })
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries(),
        "form1": form1
    }) 