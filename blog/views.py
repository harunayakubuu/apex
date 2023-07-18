from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Post
from .forms import PostCreateForm, PostUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def public_posts(request):
    posts = Post.objects.order_by('-created_at').filter(is_active=True)
    paginator = Paginator(posts, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj
    }
    return render(request, 'blog/public-posts.html', context)


def public_post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.order_by('-created_at').filter(category=post.category).exclude(id=post.id)[:6]
    context = {
        'post':post,
        'related_posts': related_posts
    }
    return render(request, 'blog/public-post-detail.html', context)


@login_required
def all_posts(request):
    posts = Post.objects.order_by('-created_at')
    # paginator = Paginator(posts, 10) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {
        # 'page_obj':page_obj
        'posts': posts
    }
    return render(request, 'blog/all-posts.html', context)


@login_required
def post_create(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            # form.save()
            messages.success(request, 'Saved.')
            return redirect('blog:all-posts')
    context = {
        'form': form
    }
    return render(request, 'blog/post-create.html', context)


@login_required
def post_update(request, id):
    post = Post.objects.get(id = id)
    update_form = PostUpdateForm(instance = post)
    if request.method == 'POST':
        update_form = PostUpdateForm(request.POST, request.FILES, instance = post)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('blog:all-posts')
    context = {
        'update_form': update_form,
        'post': post
    }
    return render(request, 'blog/post-update.html', context)


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id = id)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('blog:all-posts')