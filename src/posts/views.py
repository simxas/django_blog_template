from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, CategoryToPost
from django.db.models import Q
from django.utils import timezone

# Search function
def search(request, queryset_list, query):
    today = timezone.now().date()
    categories_list = Category.objects.all()
    queryset_list = queryset_list.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__first_name__icontains=query) |
        Q(author__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "title": query,
        "categories_list": categories_list,
        "page_request_var": page_request_var,
        "posts": queryset,
        "today": today,
    }
    return {"template": "post_search.html", "context": context}

# Posts list view
def posts_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    categories_list = Category.objects.all()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    # using this for search
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    paginator = Paginator(queryset_list, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "posts": queryset,
        "categories_list": categories_list,
        "title": "Prisijunges",
        "page_request_var": page_request_var,
        "today": today,
    }

    return render(request, "posts_list.html", context)

# Post detail view
def post_detail(request, slug):
    today = timezone.now().date()
    instance = get_object_or_404(Post, slug=slug)
    categories_list = Category.objects.all()

    # searc part
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        search_dict = search(request, queryset_list, query)
        return render(request, search_dict["template"], search_dict["context"])

    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {
        "title": instance.title,
        "instance": instance,
        "categories_list": categories_list,
        "today": today,
        "slug": slug,
    }
    return render(request, "post_detail.html", context)

# Posts category view
def post_category(request, slug):
    context = {
        "title": "post category",
    }
    return render(request, "post_category.html", context)

# Create Post view
def post_create(request):
    context = {
        "title": "post create",
    }
    return render(request, "post_form.html", context)

# Update Post view
def post_update(request, slug):
    context = {
        "title": "update post",
    }
    return render(request, "post_form.html", context)

# Delete Post view
def post_delete(request, slug=None):
    context = {
        "title": "delete post",
    }
    return redirect("posts:list")
