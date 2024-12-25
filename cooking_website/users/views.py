from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FoodPost, Step
from django.core.paginator import Paginator


def signup_login(request):
    signup_error = None
    signup_success = None
    login_error = None

    if request.method == "POST":
        # Check if the user is signing up
        if 'signup' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                signup_error = "Username already exists."
            elif User.objects.filter(email=email).exists():
                signup_error = "Email is already in use."
            else:
                # Create new user
                User.objects.create_user(username=username, password=password, 
                                         first_name=first_name, last_name=last_name, email=email)
                signup_success = "Signup successful! You can now log in."

        # Check if the user is logging in
        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
            else:
                login_error = "Invalid username or password."

    return render(request, 'users/signup_login.html', {
        'signup_error': signup_error,
        'signup_success': signup_success,
        'login_error': login_error,
    })


# Logout view
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('signup_login')  # Redirect to login page after logout

@login_required
def food_detail(request, id):
    # Fetch the specific food post and its steps
    food_post = get_object_or_404(FoodPost, id=id)
    steps = food_post.steps.all()  # Fetch all related steps for the post

    # Pass the food post and steps to the template
    return render(request, 'users/food_detail.html', {'food': food_post, 'steps': steps})


@login_required
def post_food(request):
    if request.method == 'POST':
        # Collecting basic information for the food post
        title = request.POST['title']
        description = request.POST['description']
        summary = request.POST.get('summary', '')  # Optional field

        # Creating the FoodPost object
        food_post = FoodPost.objects.create(
            title=title,
            description=description,
            summary=summary,
            user=request.user
        )

        # Save the steps in the Step model
        instructions = request.POST.getlist('instruction[]')
        reasons = request.POST.getlist('reason[]')
        for i, instruction in enumerate(instructions):
            Step.objects.create(
                food_post=food_post,
                step_number=i + 1,
                instruction=instruction,
                reason=reasons[i] if i < len(reasons) else ''
            )

        # Redirect after successful post creation
        return redirect('home')

    return render(request, 'users/post_food.html')

@login_required
def home(request):
    # Fetch all food posts and order them by creation date (newest first)
    food_posts_list = FoodPost.objects.all().order_by('-created_at')

    # Set up pagination
    paginator = Paginator(food_posts_list, 6)  # Show 6 food posts per page
    page_number = request.GET.get('page')  # Get the page number from the request
    food_posts = paginator.get_page(page_number)  # Get the corresponding page of food posts

    # Return the page with the paginated food posts
    return render(request, 'users/home.html', {'food_posts': food_posts})

@login_required
def delete_food(request, id):
    # Get the food post to delete
    food_post = get_object_or_404(FoodPost, id=id)

    # Check if the current user is the owner of the food post
    if food_post.user == request.user:
        food_post.delete()
        messages.success(request, "Food post deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this post.")

    return redirect('home')  # Redirect back to the home page
