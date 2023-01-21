from django.shortcuts import render,HttpResponse,redirect
from home.models import contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request):
    allposts=Post.objects.all()
    context={'allposts':allposts}
    return render(request,'home/home.html',context)
     
def Contact(request):
    
    
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"please fill the form correctly")
        else:    
         conta=contact(name=name,email=email,phone=phone,content=content)    
         conta.save()
         messages.success(request,"your form filled sucessfully")
         
    return render(request,'home/contact.html')
    #return HttpResponse("thi sis contact")

def about(request):
    return render(request,'home/about.html')
    #return HttpResponse("thoi sis about")

def search(request):
    query=request.GET['query'] #this is not query set 
    if len(query)>78:
        allPosts=Post.objects.none()#this will allposts a blank  query set
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)#this is use for combining two or more query set
    if allPosts.count()==0: #this this is use to calculate the length of query set
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html',params)
  
  

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>10:
            messages.error(request,"username must be less than 10 char")
            return redirect('home')
        
        if not username.isalnum() :
            messages.error(request,"username sholud contain letters and numbers only")
            return redirect('home')
        
        if pass1 !=pass2:
            messages.error(request,"password donot match")
            return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404-Not found")  
    
def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")
    else:
        
        return HttpResponse("404-Not found")
    
def handleLogout(request): 
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')   
    
    
    
    