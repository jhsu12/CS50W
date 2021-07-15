import re
from django.shortcuts import redirect, render
from markdown2 import Markdown
from django import forms
from . import util
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
      "placeholder": "Enter Page Content using Github Markdown"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    md = util.get_entry(title)
    if md == None:##entry doesn't exist
        return render(request, "encyclopedia/error.html", {
            "title": title,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "new": False,
            "markdown": Markdown().convert(md)
        })

def Search(request):
    value = request.GET.get('q')
    md = util.get_entry(value)
    

    if md is not None:##entry exist
        return redirect('encyclopedia:title', title= value)
    else: #substring of entry
        sub = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                sub.append(entry)
        
        if len(sub) != 0:
            return render(request, "encyclopedia/search_result.html", {
                "title": value,
                "have_entries": True,
                "entries": sub,
            })
        else:
            return render(request, "encyclopedia/search_result.html", {
            "title": value,
            "have_entries": False,
            
            })

def Create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            #check whether the title is existed
            entries = util.list_entries()
            for entry in entries:
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/create_new.html", {
                        "form": NewPageForm(initial={'content': content}),
                        "error": True,
                        "title":title,
                    })
            
            #if not then create new one and redirect to new page
            util.save_entry(title, content)
            md = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "new": True,
                "title": title,
                "markdown": Markdown().convert(md)
            })
    #if request.method is GET    
    return render(request, "encyclopedia/create_new.html", {
        "form": NewPageForm(),
        "error": False
    }) 

def Edit(request):

    if request.method == "GET":
        #get the title and the original markdown
        title = request.GET.get("title")
        md = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                        "title": title,
                        "form": NewPageForm(initial={'title': title, 'content': md}),
                        "error": False,
                    })
    #request.method == post
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            edit_title = form.cleaned_data["title"]
            edit_content = form.cleaned_data["content"]

            util.save_entry(edit_title, edit_content)
            md = util.get_entry(edit_title)
            return render(request, "encyclopedia/entry.html", {
                "title": edit_title,
                "new": False,
                "markdown": Markdown().convert(md)
            })

def Random(request):
    entries = util.list_entries()
    r = random.randrange(0, len(entries))

    return redirect('encyclopedia:title', title= entries[r])
    
    