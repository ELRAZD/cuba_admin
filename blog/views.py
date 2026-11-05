from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    return render(request, 'blog/blog.html', {'posts': posts_page})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db(fields=['views'])
    comments = post.comments.filter(is_approved=True, parent=None)
    form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass
            comment.save()
            messages.success(request, 'نظر شما ثبت شد و پس از تأیید نمایش داده می‌شود.')
            return redirect('blog:detail', slug=slug)
    return render(request, 'blog/blog_single.html', {
        'post': post, 'comments': comments, 'form': form,
    })


@login_required
def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        messages.success(request, 'پست با موفقیت ایجاد شد.')
        return redirect('blog:detail', slug=post.slug)
    return render(request, 'blog/add_post.html', {'form': form})
