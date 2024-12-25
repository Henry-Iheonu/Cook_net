from django.db import models
from django.contrib.auth.models import User

class FoodPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    procedures = models.TextField()  # Stores steps/procedures as plain text
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# Step model to store each step of the recipe
class Step(models.Model):
    food_post = models.ForeignKey(FoodPost, related_name='steps', on_delete=models.CASCADE)  # Each step is related to a food post
    step_number = models.PositiveIntegerField()  # Number of the step
    instruction = models.TextField()  # Instructions for the step
    reason = models.TextField(blank=True)  # Reason for the step (optional)

    class Meta:
        ordering = ['step_number']  # Automatically order steps by their step number

    def __str__(self):
        return f"Step {self.step_number} for {self.food_post.title}"

# Comment model to store comments on a food post
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # To associate a comment with a user
    food_post = models.ForeignKey(FoodPost, related_name='comments', on_delete=models.CASCADE)  # To associate a comment with a food post
    text = models.TextField()  # The content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time when the comment is created

    def __str__(self):
        return f"Comment by {self.user.username} on {self.food_post.title}"

