from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm, ContactForm


# Note: the code has been used from the CI tutorial
# I Think Therefore I Blog
# to help the setup and creation of this project.


class PostList(generic.ListView):
    # view for the post list
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):
    # view for the post detail
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):
    # view for the post likes
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def about(request):
    # view to return the about me page
    return render(request, 'about.html')


def search(request):
    # view to return the search page
    if request.method == "POST":
        searched = request.POST.get('searched', None)
        results = Post.objects.filter(title__icontains=searched)
        return render(
            request,
            'search.html',
            {
                'searched': searched,
                'results': results
            }
        )
    else:
        return render(request, 'search.html')


def contact(request):
    # view to return contact page
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact_success.html')

    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)


@login_required
def add_post(request):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added post!')
            return redirect('home')
        else:
            messages.error(request,
                           'Failed to add post. '
                           'Please ensure the form is valid.')
    else:
        form = PostForm()

    template = 'add_post.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_post(request, slug, *args, **kwargs):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated post!')
            return redirect(reverse('post_detail', args=[slug]))
        else:
            messages.error(request,
                           'Failed to update post. Please ensure the form '
                           'is valid.')
    else:
        form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.title}')

    template = 'edit_post.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)


@login_required
def delete_post(request, slug, *args, **kwargs):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can do that.')
        return redirect(reverse('home'))

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect(reverse('home'))
