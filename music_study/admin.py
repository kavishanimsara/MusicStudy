from django.contrib import admin
from .models import Profile,Category, StudySession, StudyLog

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'nic_number', 'contact_number')  # Fields to display in the admin list view
    search_fields = ('user__username', 'nic_number', 'contact_number')  # Enable search functionality
    list_filter = ('gender',)  # Filter options in the sidebar
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # Display these fields in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field

# Customizing the admin interface for the StudySession model
@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'duration', 'date',)  # Fields to display in the list view
    list_filter = ('date', 'category')  # Filter options in the sidebar
    search_fields = ('user__username', 'category__name')  # Enable search by user and category names

# Customizing the admin interface for the StudyLog model
@admin.register(StudyLog)
class StudyLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'study_duration', 'mood_before', 'mood_after', 'logged_at')  # Fields to display
    list_filter = ('logged_at', 'mood_before', 'mood_after')  # Filters in the sidebar
    search_fields = ('user__username', 'tasks_completed')  # Search by username and tasks completed
    ordering = ('-logged_at',)  # Order entries by the most recent log