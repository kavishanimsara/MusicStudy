from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudyLogForm,UserRegistrationForm, ProfileForm,UserUpdateForm
from .models import StudyLog,Category
import requests
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import StudyLog, StudySession
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.db import transaction


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')




def signup_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():  # Ensure atomic save
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user  # Link the profile to the user
                profile.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            messages.success(request, "Signup successful! Please log in to continue.")
            logout(request)  # Log the user out after signup
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def music_categories(request):
    categories = [
        {'name': 'Focus', 'description': 'Music to help you focus'},
        {'name': 'Relax', 'description': 'Relaxing music'},
        {'name': 'Energetic', 'description': 'Boost your energy'},
    ]
    return render(request, 'categories.html', {'categories': categories})

@login_required
def study_tracker(request):
    if request.method == 'POST':
        form = StudyLogForm(request.POST)
        if form.is_valid():
            study_log = form.save(commit=False)
            study_log.user = request.user
            study_log.save()
            return redirect('study_tracker')
    else:
        form = StudyLogForm()
    
    # Retrieve logged sessions for the current user
    study_logs = StudyLog.objects.filter(user=request.user).order_by('-logged_at')

    return render(request, 'study_tracker.html', {'form': form, 'study_logs': study_logs})

def about(request):
    return render(request, 'about.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')  



@login_required
def music_categories_view(request):
    categories = [
        {'type': 'Classical', 'image': '/static/images/Classical.jpeg'},
        {'type': 'Lo-fi', 'image': '/static/images/lo-fi.jpeg'},
        {'type': 'Jazz', 'image': '/static/images/Jazz.jpg'},
        {'type': 'Pop', 'image': '/static/images/Pop.jpeg'},
    ]

    search_results = []
    query = request.GET.get('q', None)

    if query:
        youtube_api_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': f"{query} music",  # Add 'music' to the search query
            'type': 'video',
            'videoCategoryId': '10',  # Music category
            'safeSearch': 'moderate',
            'key': settings.YOUTUBE_API_KEY,
            'maxResults': 10,  # Limit the number of results
        }
        response = requests.get(youtube_api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            search_results = [
                {
                    'title': item['snippet']['title'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'videoId': item['id']['videoId'],
                }
                for item in data.get('items', [])
                if 'music' in item['snippet']['title'].lower() or 'song' in item['snippet']['title'].lower()
                and item['snippet']['liveBroadcastContent'] == 'none'  # Exclude live streams
            ]

    return render(request, 'music_categories.html', {
        'categories': categories,
        'search_results': search_results,
    })


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Basic response logic
        if "hello" in user_message.lower():
            reply = "Hi there! How can I assist you today?"
        elif "music" in user_message.lower():
            reply = "Looking for music recommendations? Check out our categories!"
        elif "study" in user_message.lower():
            reply = "Try using our study tracker for better focus!"
        elif "focus" in user_message.lower():
            reply = "Listening to focus music can help you stay concentrated. Try our focus music category!"
        elif "relax" in user_message.lower():
            reply = "For relaxation, we recommend calming music or nature sounds. Let me know what you'd like!"
        elif "productivity" in user_message.lower():
            reply = "Boost your productivity by listening to upbeat music or using a timer while you work."
        elif "wellness" in user_message.lower():
            reply = "For wellness, try mindfulness music or guided meditation. Take care of your well-being!"
        elif "sleep" in user_message.lower():
            reply = "Need help sleeping? Try our sleep playlist for a restful night."
        elif "motivation" in user_message.lower():
            reply = "Motivational music can give you the boost you need. Check out our motivational category!"
        elif "workout" in user_message.lower():
            reply = "Need some workout music? Our playlist for high-energy tracks will keep you moving!"
        elif "study tips" in user_message.lower():
            reply = "Try setting a timer for study sessions and listening to instrumental music to maintain focus!"
        elif "stress" in user_message.lower():
            reply = "Listening to calming sounds or classical music can help reduce stress and anxiety."
        elif "concentration" in user_message.lower():
            reply = "Concentration music, such as binaural beats, might help you stay focused during tasks."
        elif "mood" in user_message.lower():
            reply = "Music is a great way to change your mood! Let me know if you'd like a playlist for a specific mood."
        elif "energy" in user_message.lower():
            reply = "Upbeat music with fast tempos can help increase your energy and motivation!"
        elif "creativity" in user_message.lower():
            reply = "Listening to ambient or instrumental music can help spark creativity and inspiration!"
        elif "study break" in user_message.lower():
            reply = "It's important to take breaks! Try relaxing music to unwind during your study breaks."
        elif "calm" in user_message.lower():
            reply = "Calming music or nature sounds are perfect for reducing anxiety and promoting relaxation."
        elif "well-being" in user_message.lower():
            reply = "For overall well-being, try a mix of calming and uplifting music to balance your mood."
        elif "happiness" in user_message.lower():
            reply = "Music can boost happiness! Try listening to cheerful and lively songs to lift your spirits."
        elif "focus tips" in user_message.lower():
            reply = "Consider using focus playlists with non-distracting, steady rhythms to keep you in the zone."
        elif "creativity boost" in user_message.lower():
            reply = "Ambient or classical music is great for boosting creativity, especially if you’re working on a project!"
        else:
            reply = "I'm here to help with any questions about music, productivity, relaxation, and well-being!"


        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def user_profile(request):
    user = request.user
    study_logs = StudyLog.objects.filter(user=user).order_by('-logged_at')
    study_sessions = StudySession.objects.filter(user=user).order_by('-date')

    context = {
        'user': user,
        'study_logs': study_logs,
        'study_sessions': study_sessions,
    }
    return render(request, 'profile.html', context)


@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    profile = user.profile  # Access the related Profile model

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')  # Redirect to avoid form resubmission
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def study_tracker(request):
    if request.method == "POST":
        # Fetch data from the frontend
        category_id = request.POST.get('category_id')
        mood_before = request.POST.get('mood_before', 'Neutral')
        mood_after = request.POST.get('mood_after', 'Neutral')

        # Create or fetch the category
        category = Category.objects.get(id=category_id)

        # Create a StudySession
        StudySession.objects.create(
            user=request.user,
            category=category,
        )

        # Create a StudyLog
        StudyLog.objects.create(
            user=request.user,  
            mood_before=mood_before,
            mood_after=mood_after,
        )


    categories = Category.objects.all()
    return render(request, 'study_tracker.html', {'categories': categories})

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import StudyLog

@receiver(user_logged_in)
def create_study_log(sender, request, user, **kwargs):
    StudyLog.objects.create(user=user, study_duration=0)
    
      # Set duration to 0 initially

@login_required
def admin_redirect(request):
    if request.user.is_staff:  # Only allow admin users
        return redirect('/admin/')
    else:
        return redirect('/')  # Redirect non-admin users to the homepage

