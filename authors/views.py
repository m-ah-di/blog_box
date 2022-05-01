from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.


def register(request):
    """User registration form/functionality"""
    if request.method != 'POST':
        # Create a blank form.
        form = UserCreationForm()
    else:
        # Otherwise, process data.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log in the new user and redirect to home.
            login(request, new_user)
            return redirect('blogs:your_articles')
    # Display the already created blank form.
    context = {'sign_up_form': form}
    return render(request, 'registration/register.html', context)
