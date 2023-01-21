from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,Blogcomment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
# Create your views here.
def bloghome(request):
    
    allPosts=Post.objects.all() #this will give all objects in django admin of Posts in query set
    context={'allPosts':allPosts}
    return render(request,'blog/bloghome.html',context)
   # return HttpResponse('this is bloghome')

def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()#as this is query set and have only one object at first palce so to acess it we use first()
   # print(post)
    comments=Blogcomment.objects.filter(post=post,parent=None)
    replies=Blogcomment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:                                                                                                                                   
            replyDict[reply.parent.sno].append(reply)
    print(replyDict)                
    context={'post':post,'comments':comments,'user':request.user,'replyDict':replyDict} #as ther is only one object in post ,as for one slug we have only one object so no need to use for loop in template of it
    return render(request,'blog/blogPost.html',context)
    #return HttpResponse(f'this is blog post{slug}')

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=Blogcomment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Blogcomment.objects.get(sno=parentSno)
            comment=Blogcomment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/blog/{post.slug}")        
                