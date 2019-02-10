# This file is part of onepageblog.
# 
# onepageblog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# onepageblog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with onepageblog.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_managers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from posts.forms import PostForm, UserChangeForm
from posts.models import Post


class PostListView(ListView):
    context_object_name = 'post_list'
    
    def get_queryset(self):
        """If the user is a member of the Moderators group, show all posts,
        otherwise just show published posts.
        """
        if (
                hasattr(self.request, 'user') and
                self.request.user.is_authenticated() and
                self.request.user.groups.filter(name='Moderators').count()
        ):
            return Post.objects.all()
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    context_object_name = 'post'
    
    def get_queryset(self):
        """Allow moderators to see unpublished posts.
        """
        if (
                hasattr(self.request, 'user') and
                self.request.user.is_authenticated() and
                self.request.user.groups.filter(name='Moderators').count()
        ):
            return Post.objects.all()
        return Post.objects.filter(is_published=True)


def register(request):
    """Uses standard register form
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=request.POST['username'], 
                                     password=request.POST['password1'])
            auth.login(request, user)
            return HttpResponseRedirect(reverse('post_list_view'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {'form': form})


def logout(request):
    """Logs out and redirects to the post list.
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('post_list_view'))


@login_required
@csrf_protect
def add_post(request):
    """Submit a new post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Save the submission
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            # Notify managers of new submission
            c = Context({'post': post})
            t = loader.get_template('posts/post_email.txt')
            text_message = t.render(c)
            t = loader.get_template('posts/post_email.html')
            html_message = t.render(c)
            mail_managers('New post submission', text_message,
                          fail_silently=True, html_message=html_message)
            # Confirm submission
            messages.success(request, 
                             'Thank you. Your post has been submitted.')
            return HttpResponseRedirect(reverse('post_list_view'))
    else:
        form = PostForm()
    return render(request, 'posts/post_add.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'registration/profile.html')


@login_required
@csrf_protect
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=False)
            return HttpResponseRedirect(reverse('post_list_view'))
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})
