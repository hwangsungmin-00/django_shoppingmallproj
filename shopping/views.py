from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Manufacture, Comment
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

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

# Create your views here.

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model =Post
    fields = ['title', 'price', 'volume', 'content', 'packing', 'head_image', 'category', 'manufacture']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser) :
            form.instance.author = current_user
            return super(PostCreate,self).form_valid(form)
        else :
            return redirect('/shopping/')

class PostUpdate(LoginRequiredMixin,UpdateView): # 모델명_form
    model = Post
    fields = ['title', 'price', 'volume', 'content', 'packing', 'head_image', 'category', 'manufacture']

    template_name = 'shopping/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

class PostList(ListView) :
    model = Post
    ordering = 'pk'
    paginate_by = 8
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['manufactures'] = Manufacture.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

#    template_name = 'shopping/post_list.html'
#post_list.html

class PostDetail(DetailView) :
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['manufactures'] = Manufacture.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

#post_detail.html

class PostSearch(PostList) :
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q}({self.get_queryset().count()})'

        return context

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

def manufacture_page(request, slug):
    if slug == 'no_manufacture' :
        manufacture = '미분류'
        post_list = Post.objects.filter(manufacture=None)
    else :
        manufacture = Manufacture.objects.get(slug=slug)
        post_list = Post.objects.filter(manufacture=manufacture)
    return render(request, 'shopping/post_list.html',
                  {
                      'post_list' : post_list,
                      'manufactures' : Manufacture.objects.all(),
                      'no_manufacture_post_count' : Post.objects.filter(manufacture=None).count(),
                      'manufacture' : manufacture
                  }
                  )

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model=Comment
    form_class=CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post=comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

#def index(request) :
#    posts = Post.objects.all().order_by('pk')
#    return render(request, 'shopping/post_list.html',
#                  {
#                      'posts' : posts
#                  }
#                  )

#def single_post_page(request, pk) :
#    post = Post.objects.get(pk=pk)
#
#    return render(request, 'shopping/post_detail.html',
#                  {
#                      'post': post
#                  }
#                  )