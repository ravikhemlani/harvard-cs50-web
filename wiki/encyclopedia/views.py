from django.shortcuts import render, redirect
from .forms import WikiPage, EditPage
from django.contrib import messages
from random import randint
from . import util
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def render_page(request, title):
    entry = util.get_entry(title.strip())
    if entry is None:
        entry = "#Page not found"
    entry = markdown(entry)
    return render(request, "encyclopedia/page.html", {
        "entries": entry, "title": title})


def create_page(request):
    if request.method == "POST":
        form = WikiPage(request.POST)
        if form.is_valid():
            instance = form.cleaned_data
            if not util.get_entry(instance["title"]):
                util.save_entry(instance["title"], instance["markdown_content"])
                messages.success(request, "{} successfully added".format(instance["title"]))
                return redirect('index')
            else:
                messages.warning(request, "Page with the same title already exists. Please use another title.")
    else:
        form = WikiPage()
    return render(request, 'encyclopedia/create.html', {'form': form})


def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)


def edit_page(request, title):
    if request.method == "POST":
        form = EditPage(request.POST)
        if form.is_valid():
            instance = form.cleaned_data
            util.save_entry(title, instance["markdown_content"])
            messages.success(request, "{} successfully edited".format(title))
            return redirect('index')
    else:
        form = EditPage(initial={"markdown_content": util.get_entry(title)})
    return render(request, 'encyclopedia/edit.html', {'form': form, 'title': title})


def search_results(request):
    q = request.GET.get("q")
    entry_list = [entry.lower() for entry in util.list_entries()]
    if q.lower() in entry_list:
        return redirect("entry", q)
    return render(request, 'encyclopedia/search.html', {'entries': util.search(q), 'q': q})
