from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from .models import post,Contact
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
import math
# Create your views here.
def home(request):
     posts=post.objects.all()[1:4]
     return render(request,'blog/home.html',{'posts':posts})


def about(request):
     return render(request,'blog/about.html')

def blog(request):
      no_of_post=3
      page=request.GET.get('page')
      if page is None:
            page=1
      else:
            page=int(page)      
      blogs=post.objects.all()
      length=len(blogs)
      blogs=blogs[(page-1)*no_of_post:page*no_of_post]
      if page>1:
         prev=page-1
      else:
           prev=None
      if page<math.ceil(length/no_of_post):        
        nxt=page+1
      else:
           nxt=None  
      context={
            'blogs':blogs,
            'prev':prev,
            'nxt':nxt
      }
      return render(request,'blog/bloghome.html',context)

def blogpost(request,id):
     posts=post.objects.get(pk=id)
     context={'posts':posts}
     return render(request,'blog/blogpost.html',context) 


def contact(request):
   try:  
     message=False
     data={}
     if request.method=="POST":
           name=request.POST.get("name")
           email=request.POST.get('email')
           phone=request.POST.get('phone')
           desc=request.POST.get('desc')
           instance=Contact(name=name,email=email,phone=phone,desc=desc)
           instance.save()
           data={
                'message':True 
           }
     return render(request,'blog/contact.html',data)
   except:
       return render(request,'blog/contact.html') 

    

# logout
def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/')


def user_signup(request):
     if request.method=="POST":
          form=SignUpForm(request.POST)
          if form.is_valid():
               messages.success(request,'Congratulations! You have become an Author.')
               user=form.save()
               group=Group.objects.get(name="Author")
               user.groups.add(group)
               form=SignUpForm()
               return redirect('/login/')
     else:     
            form=SignUpForm()
     return render(request,'blog/signup.html',{'form':form})


def user_login(request):
    try:
        if not request.user.is_authenticated:
            if request.method == "POST":
                form = LoginForm(request, data=request.POST)
                if form.is_valid():
                    uname = form.cleaned_data['username']
                    upass = form.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Logged in Successfully!')
                        return HttpResponseRedirect('/thanks/')
                    else:
                        messages.error(request, 'Invalid credentials, please try again.')
                else:
                    messages.error(request, 'Invalid form submission.')
            else:
                form = LoginForm()
            return render(request, 'blog/login.html', {'form': form})
        else:
            return HttpResponseRedirect('/thanks/')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return HttpResponseRedirect('/thanks/')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                # Create the post instance without saving it to the database
                pst = form.save(commit=False)
                
                # Set the author to the logged-in user
                pst.author = request.user
                
                # Save the post instance to the database
                pst.save()
                messages.success(request, 'Your post has been added successfully! <a href="/dashboard/">Go to Dashboard</a>')
                # Optional: Clear the form after saving
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')
       

def search(request):
      if request.method=="GET":
           st=request.GET.get('post_title')
           if st!=None:
                data=post.objects.filter(title__icontains=st)
      context={
           'data':data
      }          
      return render(request,'blog/search.html',context)

def thankyou(request):
     if request.user.is_authenticated:
        user=request.user
        full_name=user.get_full_name()
        data={
              'full_name':full_name,
              }
     return render(request,'blog/thanks.html',data)


from django.shortcuts import render, get_object_or_404

def update_post(request, id):
    if request.user.is_authenticated:
        post_instance = get_object_or_404(post, pk=id)

        if request.method == "POST":
            form = PostForm(request.POST, instance=post_instance)
            if form.is_valid():
                form.save()
                # Add a success message using the messages framework
                messages.success(request, 'Post updated successfully! <a href="/dashboard/">Go to Dashboard</a>')
                form=PostForm(instance=post_instance)
                # Redirect to the same page with a fresh empty form
                return HttpResponseRedirect(f'/updatepost/{id}/')  # Redirect to the update page to clear the form

        else:
            form = PostForm(instance=post_instance)

        data = {
            'form': form
        }
        return render(request, 'blog/update.html', data)

    return HttpResponseRedirect('/login/')


def delete_post(request,id):
     if request.user.is_authenticated:
          if  request.method=="POST":
                pi=post.objects.get(pk=id) 
                pi.delete()   
                messages.success(request,"Your post deleted Successfully! ") 
                return HttpResponseRedirect('/dashboard/')   
     else:
          return HttpResponseRedirect('/login/')    
     
from django.contrib.auth.decorators import login_required
def dashboard(request):
    posts = post.objects.filter(author=request.user)  # Filter posts by logged-in user
    user = request.user
    full_name = user.get_full_name()
    gps = user.groups.all()
    
    data = {
        'posts': posts,
        'full_name': full_name,
        'groups': gps
    }
    
    return render(request, 'blog/dashboard.html', data)