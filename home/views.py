from django.shortcuts import render, HttpResponse, redirect
from home.models import Contactcode
from blog.models import Postcode
from django.contrib import  messages
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User 

# Create your views here.
def home(request):
    return render(request, 'home/home.html')



def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message =request.POST['message']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
           messages.error(request, "Please fill the form correctly")
        else:
            contact=Contactcode(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
            return render(request, 'home/home.html')
    return render(request, 'home/home.html')


def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Postcode.objects.none()
    else:
        allPostsTitle= Postcode.objects.filter(title__icontains=query)
        allPostsAuthor= Postcode.objects.filter(author__icontains=query)
        allPostsContent =Postcode.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)



def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username= request.POST['username'].lower()
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
          

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
          
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your CodeWizards has been successfully created")
        return redirect('home')

    else:
        return render(request, 'home/signup.html')
def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername'].lower()
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            
            return render(request, 'home/signin.html')


    return render(request, 'home/signin.html')
   

    # return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

