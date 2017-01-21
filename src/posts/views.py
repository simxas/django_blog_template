from django.shortcuts import render, get_object_or_404, redirect

# Posts list view
def posts_list(request):
    context = {
        "title": "posts list",
    }
    return render(request, "posts_list.html", context)

# Post detail view
def post_detail(request, slug):
    context = {
        "title": "post detail",
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
