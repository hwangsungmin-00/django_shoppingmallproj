from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from shopping.forms import CommentForm
from shopping.models import Post, Category, Comment


# Create your views here.


def langing(request):
    recent_posts=Post.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {'recent_posts' : recent_posts})

def my_page(request):
    comment_list = Comment.objects.filter(author=request.user)
    return render(request,
                  'single_pages/my_page.html',
                  {
                      'comment_list': comment_list,
                  })

def my_company(request):
    return render(request, 'single_pages/my_company.html')

def category_page(request, slug):
    if slug == 'no_category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request, 'shopping/post_list.html',
                  {
                      'post_list' : post_list,
                      'categories' : Category.objects.all(),
                      'no_category_post_count' : Post.objects.filter(category=None).count(),
                      'category' : category
                  }
                  )

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST' :
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else :
            return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied