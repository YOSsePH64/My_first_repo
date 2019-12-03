from django.shortcuts import render , get_object_or_404
from .models import Post
from django.utils import timezone
# Create your views here.
from django.shortcuts import redirect
from .forms import PostForm
from django.utils import timezone
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return  render(request , 'blog/post_list.html' , {'posts' : posts})

# def post_detail(request , pk):
# 	post = get_object_or_404(Post , pk=pk)
# 	return render(request , 'blog/post_detail.html' , {'post' : post})

# Written By Me works  well as the above one , may not be better since less is more
def post_detail(request , pk):
	posts = Post.objects.all()
	ids = []
	for post in posts:
		ids.append(post.id)
	flag = True
	for post in posts:
		if pk == post.pk:
			flag = True
			return render(request , 'blog/post_detail.html' , { 'post' : post})
		else:
			flag = False 
	if flag == False:
		return render(request , 'blog/error.html' , {'post' : post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail' , pk=post.pk)
    else:
        form = PostForm()

    return render(request , 'blog/post_edit.html' , {'form' : form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html' , {'form' : form})
