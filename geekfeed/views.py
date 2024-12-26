from django.shortcuts import render,redirect,get_object_or_404
from .models import Technology,Gamer,Blog,Message
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from .forms import MessageForm






def home(request):
    technology_posts = Technology.objects.all().order_by('-created_at')
    game_posts = Gamer.objects.all().order_by('-created_at')
    user_posts = Blog.objects.all().order_by('-created_at')

    context = {
        'technology_posts': technology_posts,
        'game_posts': game_posts,
        'user_posts': user_posts,
    }
    
    return render(request, 'geekfeed/home.html', context)

def base(request):
    return render(request,"geekfeed/base.html")


def technology(request):
    
    technologies = Technology.objects.all()
    return render(request, 'geekfeed/technology.html', {'technologies': technologies})



def technology_detail(request, tech_id):
    tech_post = Technology.objects.get(id=tech_id)
    return render(request, 'geekfeed/technology_detail.html', {'tech_post': tech_post})



def games(request):
    gamer = Gamer.objects.all()
    return render(request,'geekfeed/games.html', {'gamer': gamer})


def games_detail(request,game_id):
    games_post = Gamer.objects.get(id=game_id)
    return render(request,'geekfeed/games_detail.html',{'games_post': games_post})


def contact(request):
    return render(request,"geekfeed/contact.html")







def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
            else:
              
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Cuenta creada con éxito. Ahora puedes iniciar sesión.')
                return redirect('login')  
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'geekfeed/signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, 'Credenciales Incorrectas')
    return render(request, 'geekfeed/login.html')
    

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        
        if not request.user.check_password(old_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('change_password') 

        
        if new_password != confirm_new_password:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            return redirect('change_password')  

        user = request.user
        user.set_password(new_password)
        user.save()

        
        update_session_auth_hash(request, user)

        messages.success(request, 'Contraseña cambiada con éxito.')
        return redirect('login')  

    return render(request, "geekfeed/change_password.html")



@login_required
def dashboard(request):
   
    user = request.user
    return render(request, "geekfeed/dashboard.html", {"user": user})



@login_required
def dashboard(request):
    
    form = BlogForm()
    
    if request.method == 'POST':
        
        if 'create' in request.POST:
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user  
                blog.save()
                messages.success(request, 'Post creado con éxito.')
                return redirect('dashboard')
            else:
                
                messages.error(request, 'Error al crear el post. Por favor, revisa los campos.')
        
  
        
        
        elif 'delete' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Blog, id=post_id, author=request.user)
            post.delete()
            messages.success(request, 'Post eliminado con éxito.')
            return redirect('dashboard')

    
    posts = Blog.objects.filter(author=request.user)
    
    
    return render(request, 'geekfeed/dashboard.html', {'form': form, 'posts': posts})


@login_required
def edit_post(request, post_id):
    
    post = get_object_or_404(Blog, id=post_id, author=request.user)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()  
            return redirect('dashboard')  
    else:
        form = BlogForm(instance=post)  
    return render(request, 'geekfeed/edit_post.html', {'form': form})






@login_required
def inbox(request):
    if request.method == 'POST' and 'delete' in request.POST:
        message_id = request.POST.get('message_id')
        message = get_object_or_404(Message, id=message_id, receiver=request.user)  
        message.delete()
        return redirect('inbox')

    messages = Message.objects.filter(receiver=request.user)

    return render(request, 'geekfeed/inbox.html', {
        'messages': messages,
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')  
    else:
        form = MessageForm()

    return render(request, 'geekfeed/send_message.html', {'form': form})

@login_required
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return redirect('inbox')



@login_required
def responder_mensaje(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect("inbox")
    
    return render(request, "responder_mensaje.html", {"recipient": recipient})



def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        

        
        messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
        return redirect('contact')  

    return render(request, 'geekfeed/contact.html')