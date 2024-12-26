from django.db import models
from django.shortcuts import render, get_object_or_404
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



class Technology(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)  
    image = models.ImageField(upload_to='technology-images/')
    full_content = RichTextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title

    
def technology_detail(request, tech_id):
    
    tech_post = get_object_or_404(Technology, pk=tech_id)
    return render(request, 'geekfeed/technology_detail.html', {'tech_post': tech_post})



class Gamer(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='games-images/')
    full_content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


def games_detail(request,game_id):
    games_post = get_object_or_404(Gamer, pk=game_id)
    return render(request, 'geekfeed/games_detaail.html', {'games_post':games_post})

class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return self.title
    



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ['-created_at']



