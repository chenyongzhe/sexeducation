


from django.http import JsonResponse
from django.shortcuts import render
#wangchaojun
# Create your views here.
from django.shortcuts import  HttpResponse
from django.shortcuts import redirect
import os
import json
from article import models
from django.core.cache import cache
##from alipay import AliPay
from django.conf import settings
import datetime
import time
from django.db.models import Q
import re



def judge_qq_mobile(ua):
    """
    判断访问来源是否腾讯浏览器
    :param ua: 访问来源头信息中的User-Agent字段内容
    :return:
    """
    factor = ua
    is_QQmobile = False
    if "QQBrowser" in factor:
        is_QQmobile=True

    return is_QQmobile

def judge_pc_or_mobile(ua):
    """
    判断访问来源是pc端还是手机端
    :param ua: 访问来源头信息中的User-Agent字段内容
    :return:
    """
    factor = ua
    is_mobile = False
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp' \
                    r'|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)' \
                    r'|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)' \
                     r'|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)' \
                     r'|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw' \
                     r'|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8' \
                     r'|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit' \
                     r'|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)' \
                     r'|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji' \
                     r'|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx' \
                     r'|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi' \
                     r'|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)' \
                     r'|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg' \
                     r'|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21' \
                     r'|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-' \
                     r'|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it' \
                     r'|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)' \
                     r'|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)' \
                     r'|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit' \
                     r'|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'

    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(factor) != None:
        is_mobile = True
    user_agent = factor[0:4]
    if _short_matches.search(user_agent) != None:
        is_mobile = True

    return is_mobile










def islogin(myrequest):
    name = myrequest.COOKIES.get('username')
    logistr=""
    if name:
        user = models.ArticleUserinfor.objects.filter(username=name).first()
        logistr="""<a href="/userinfor"><img src="%s" style="width:50px;height:50px;%s"></a>""" %(user.imgurl,"border-radius:100%;")
    else:
        logistr="""<script> $("#login_img").css("top","-5px");</script><button type="button" class="btn btn-primary"  data-toggle="modal" data-target="#myModal">登录</button>"""
    return logistr

def addscore(myrequest,num):
    name = myrequest.COOKIES.get('username')
    if name:
        user = models.ArticleUserinfor.objects.filter(username=name).first()
        score=int(user.score)+num
        models.ArticleUserinfor.objects.filter(id=user.id).update(score=score)



def  index1(request):
    #result = models.Userinfor.objects.filter(username="chen").first()
    result1=models.Article.objects.filter(article_id=750).first()
    result=models.Article.objects.raw("select * from article where title like '%%男生%%'")
    return render(request, 'index1.html', {'article':result})


def index(request):
    loginstr=islogin(request)
    addscore(request,2)
    #cache.set("name","陈永喆")
    #myname=cache.get("name")
    #print(myname)
    result = models.Article.objects.all()
    count=len(result)
    num="总共"+str(count)+"篇文章"
    current_page = request.GET.get("p", 1)
    print(current_page)
    current_page = int(current_page)
    start = (current_page - 1) * 8
    end = current_page * 8
    print(result[1].title)
    result.reverse()
    print(result[1].title)
    data1 = result[count-end:count-start]
    data=list(data1)
    data.reverse()
    print(data[1].title)
    all_count = count
    total_count, y = divmod(all_count, 8)
    if y:
        total_count += 1
    page_list = []
    nav = """<nav aria-label= "Page navigation" >
        <ul class ="pagination" >"""
    page_list.append(nav)
    page_num = 7
    start_index = 1
    end_index = 0
    if total_count < page_num:
        start_index = 1
        end_index = total_count + 1
    else:
        if current_page <= ((page_num + 1) / 2):
            start_index = 1
            end_index = page_num + 1
        else:
            start_index = current_page - (page_num - 1) / 2
            end_index = current_page + (page_num + 1) / 2
            if (current_page + (page_num - 1) / 2) > total_count:
                end_index = total_count + 1
                start_index = total_count - page_num + 1
    pre = ""
    if current_page == 1:
        pre = """<li>
            <a href="#" aria-label = "Previous" >
            <span aria-hidden = "true" > &laquo; </span></a>
           </li>"""

        # pre = '<a class="page" href="#">上一页</a>'
    else:
        pre = '<li>  <a href = "/readarticle/'
        pre2 = """?p=%s" aria-label="Previous" >
                   <span aria-hidden="true" > &laquo; </span></a>
                  </li>""" % (current_page - 1)
        pre = pre + pre2
        #        print(pre)
    page_list.append(pre)

    for i in range(int(start_index), int(end_index)):
        if i == current_page:
            temp = '<li class ="active" > <a href="/readarticle?&p=%s">%s</a></li>' % (i, i)
            # temp = '<a class="page isactive" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
        else:
            # temp = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
            temp = '<li> <a href="/readarticle?p=%s">%s</a></li>' % (i, i)
        page_list.append(temp)
    afterpage = ""
    if current_page == total_count:
        # afterpage = '<a class="page" href="#">下一页</a>'
        afterpage = """<li>
                    <a href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span></a>
                   </li>"""
    else:
        afterpage = '<li>  <a href = "/readarticle?'
        afterpage2 = """p=%s" aria-label="Next" >
                           <span aria-hidden ="true">&raquo;</span></a>
                          </li>""" % (current_page + 1)
        afterpage = afterpage + afterpage2
        # afterpage = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">下一页</a>' % (current_page + 1)
        page_list.append(afterpage)
    nav2 = '</ul> </nav>'
    page_list.append(nav2)
    page_str = "".join(page_list)
    for i in range(len(data)):
        data[i].content = re.sub("[A-Za-z0-9\!\%\[\]\,\。<>/\"=-_.-: ;]", "", data[i].content)
        data[i].content=data[i].content[0:90]
    userAgent = request.META['HTTP_USER_AGENT']

    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'mmainpage.html',{'article': data, 'num': num, 'page_str': page_str, 'loginstr': loginstr})

    return render(request, 'mainpage.html', {'article': data, 'num': num, 'page_str': page_str,'loginstr':loginstr})



def search(request):
    loginstr = islogin(request)
    addscore(request, 2)
    keyword=request.GET.get("keyword",None)
    result=None
    if  keyword :
        result = models.Article.objects.raw("select distinct * from article where title like '%%"+keyword+"%%'")
    else :
       pass
    count=0
    for i in result:
        count=count+1
    num="查询到"+str(count)+"篇文章"
    #num=len(list(result))

    ###
    ##分页
    ##
    current_page = request.GET.get("p", 1)
    print(current_page)
    current_page = int(current_page)
    start = (current_page - 1) * 8
    end = current_page * 8
    data = result[start:end]
    all_count = count
    total_count, y = divmod(all_count, 8)
    if y:
        total_count += 1
    page_list = []
    nav="""<nav aria-label= "Page navigation" >
    <ul class ="pagination" >"""
    page_list.append(nav)
    page_num = 7
    start_index = 1
    end_index = 0
    if total_count < page_num:
        start_index = 1
        end_index = total_count + 1
    else:
        if current_page <= ((page_num + 1) / 2):
            start_index = 1
            end_index = page_num + 1
        else:
            start_index = current_page - (page_num - 1) / 2
            end_index = current_page + (page_num + 1) / 2
            if (current_page + (page_num - 1) / 2) > total_count:
                end_index = total_count + 1
                start_index = total_count - page_num + 1
    pre = ""
    if current_page == 1:
        pre="""<li>
        <a href="#" aria-label = "Previous" >
        <span aria-hidden = "true" > &laquo; </span></a>
       </li>"""



        #pre = '<a class="page" href="#">上一页</a>'
    else:
        pre = '<li>  <a href = "/s/?keyword='
        pre2="""&p=%s" aria-label="Previous" >
               <span aria-hidden="true" > &laquo; </span></a>
              </li>"""% (current_page - 1)
        pre = pre+keyword+pre2
        print(pre)
    page_list.append(pre)

    for i in range(int(start_index), int(end_index)):
        if i == current_page:
            temp='<li class ="active" > <a href="/s/?keyword='+keyword+'&p=%s">%s</a></li>' % (i, i)
            #temp = '<a class="page isactive" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
        else:
            #temp = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
            temp = '<li> <a href="/s/?keyword=' + keyword + '&p=%s">%s</a></li>' % (i, i)
        page_list.append(temp)
    afterpage = ""
    if current_page == total_count:
        #afterpage = '<a class="page" href="#">下一页</a>'
        afterpage = """<li>
                <a href="#" aria-label="Next">
                <span aria-hidden="true">&raquo;</span></a>
               </li>"""
    else:
        afterpage = '<li>  <a href = "/s/?keyword='
        afterpage2 = """&p=%s" aria-label="Next" >
                       <span aria-hidden ="true">&raquo;</span></a>
                      </li>"""% (current_page + 1)
        afterpage = afterpage + keyword + afterpage2
        #afterpage = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">下一页</a>' % (current_page + 1)
        page_list.append(afterpage)
    for i in range(len(data)):
        data[i].content = re.sub("[A-Za-z0-9\!\%\[\]\,\。<>/\"=-_.-: ;]", "", data[i].content)
        data[i].content = data[i].content[0:90]
    nav2='</ul> </nav>'
    page_list.append(nav2)
    page_str = "".join(page_list)
    userAgent = request.META['HTTP_USER_AGENT']

    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'mmainpage.html', {'article': data, 'num': num, 'page_str': page_str, "loginstr": loginstr})

    return   render(request, 'mainpage.html',{'article':data,'num':num,'page_str':page_str,"loginstr":loginstr})
def article(request):
    userAgent = request.META['HTTP_USER_AGENT']
    myhtml="article1.html"
    if (judge_pc_or_mobile(userAgent)):
        myhtml="marticle.html"
    loginstr = islogin(request)
    addscore(request, 2)
    myid=request.GET.get("id",None)
    myarticle=models.Article.objects.filter(article_id=myid ).first()
    #print(myarticle.title)
    comment=[]
    mycommtent = models.Comment.objects.filter(article_id=myid)
    for cc in mycommtent:
        user=models.ArticleUserinfor.objects.filter(id=cc.user_id).first()
        comment_tamp={}
        comment_tamp["username"]=user.username
        comment_tamp["user_id"]=user.id
        comment_tamp["comment_content"]=cc.comment_content
        comment_tamp["nickname"]=user.nickname
        comment.append(comment_tamp)
    comment_cookie=""
    comment_cookie = request.COOKIES.get('comment_cookie',None)

    if comment_cookie !=None and comment_cookie !="N":
      comment_cookie = json.loads(comment_cookie)
      #print(comment_cookie)
    if comment_cookie ==None or comment_cookie =='N':
             comment_cookie=""
    print(comment_cookie)
    name = request.COOKIES.get('username')
    myclass="fa fa-thumbs-o-up"
    if name:
      user = models.ArticleUserinfor.objects.filter(username=name).first()
      sp=models.Support.objects.filter(user_id=user.id, article_id=myid).first()
      if sp:
          myclass="fa fa-thumbs-up"
    origin="";
    if myarticle.origin:
        origin="内容爬取于: "+myarticle.origin

    myrender=render(request,myhtml,{'article':myarticle,'comment':comment,'comment_cookie':comment_cookie,'supportcount':myarticle.supportcount,'myclass':myclass,'origin':origin,"loginstr":loginstr})
    myrender.set_cookie('comment_cookie',"N")
    return myrender

def player(request):
    addscore(request, 2)
    url='http://player.youku.com/embed/'
    id = request.GET.get("id", None)
    url=url+str(id)
    video_list = models.Video.objects.filter(video_id=id).first()
    title=video_list.title
    return render(request,'youkuvideo.html',{'url':url,'title':title})
def videoeducation(request):
    addscore(request, 2)
    video_list = models.Video.objects.all()
    return render(request,'videoeducation.html',{'video_list':video_list})

def login(request):
    response = {}
    response['message'] = "登录成功"

    msg={}
    error = ""
    msg['username']=""
    msg['password']=""
    isredict=False
    username = request.GET.get('aid', None)
    if request.method=='GET':
        username = request.GET.get('username', None)
        password = request.GET.get('p', None)

        if username ==None and password==None:
            print("没问题")
            return json.dumps(response)
        else:
            msg['username'] = username
            msg['password'] = password
            return render(request, 'login.html',{'error': error,'msg':msg})

    if(request.method=='POST'):
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        print(username)
        print(password)
        if username == "" or password == "":
            error = "账号密码不能为空"
            response['message'] = error
            return json.dumps(response)
        else:
          user= models.ArticleUserinfor.objects.filter(username=username).first()
          if not user :
              error="该用户不存在"
              response['message'] = error
              return HttpResponse(json.dumps(response,ensure_ascii=False))

          if user.password==password :
              res = HttpResponse(json.dumps(response,ensure_ascii=False))
              res.set_cookie('username', username)
              aid = request.COOKIES.get('aid')
              print(aid)
              if aid !=None and (aid !='N'):
                  res1 = HttpResponse(json.dumps(response,ensure_ascii=False))
                  res1.set_cookie('aid', "N")
                  res1.set_cookie('username', username)
                  return res1
              return res
          error = "密码错误"
          response['message'] = error
          return  HttpResponse(json.dumps(response,ensure_ascii=False))

    else:

      return HttpResponse(json.dumps(response,ensure_ascii=False))

def userinfor(request):
    loginstr = islogin(request)
    name = request.COOKIES.get('username')
    if not name:
        userAgent = request.META['HTTP_USER_AGENT']
        # print(userAgent)
        if (judge_pc_or_mobile(userAgent)):
            return render(request, "mpleaselogin.html", {"loginstr": loginstr})
        return render(request,"pleaselogin.html",{"loginstr":loginstr})
    user=models.ArticleUserinfor.objects.filter(username=name).first()
    myarticle= models.Article.objects.filter(user_id=user.id)
    sex=""
    csssex=""
    if user.gender==0:
        sex='fa fa-mars'
        csssex="color:blue"
    else:
        sex = 'fa fa-venus'
        csssex = "color:pink"
    me = None
    followlist = []
    followerlist = []
    # followerlist = []
    followees = []
    if True:

        me = models.ArticleUserinfor.objects.filter(username=name).first()
        follows = models.Follow.objects.filter(follower=me.id)
        followlist = []

        for ff in follows:
            followee = models.ArticleUserinfor.objects.filter(id=ff.followee).first()
            followees.append(followee)
            followlist.append(ff.followee)
        followers = models.Follow.objects.filter(followee=me.id)

        for ff in followers:
            follower = models.ArticleUserinfor.objects.filter(id=ff.follower).first()
            followerlist.append(follower)

    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'muserinfor.html',
                      {'user': user, 'myarticle': myarticle, "imgurl": user.imgurl, "sex": sex, "csssex": csssex,
                       "score": user.score, "me": me, "followeelist": followees, "followerlist": followerlist,
                       "loginstr": loginstr})

    return render(request,'userinfor.html',{'user':user,'myarticle':myarticle,"imgurl":user.imgurl,"sex":sex,"csssex":csssex,"score":user.score,"me":me,"followeelist":followees,"followerlist":followerlist,"loginstr":loginstr})

def sent_aritcle(request):
    loginstr = islogin(request)
    name = request.COOKIES.get('username')

    if not name:
        userAgent = request.META['HTTP_USER_AGENT']
        # print(userAgent)
        if (judge_pc_or_mobile(userAgent)):
            return render(request, "mpleaselogin.html", {"loginstr": loginstr})
        return render(request,"pleaselogin.html",{"loginstr":loginstr})
    user = models.ArticleUserinfor.objects.filter(username=name).first()
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'msent_article.html', {'user': user, "loginstr": loginstr})

    return render(request,'sent_article.html',{'user':user,"loginstr":loginstr})

def insert_article(request):
    addscore(request, 20)
    name = request.COOKIES.get('username')
    response = {'state': True}
    try:
       title = request.POST.get('title', None)
       content = request.POST.get('content', None)
       user=user = models.ArticleUserinfor.objects.filter(username=name).first()
       models.Article.objects.create(title=title, content=content,type_id='9',user_id=user.id,supportcount=0)
       print(title)
    except :
        response['state'] = False
    return HttpResponse(json.dumps(response))

def register(request):
     loginstr = islogin(request)
     error=""
     myhtml="register.html"
     userAgent = request.META['HTTP_USER_AGENT']

     if (judge_pc_or_mobile(userAgent)):
         myhtml = "mregister.html"
     if request.method=='POST':
        try:
           username = request.POST.get('username', None)
           password1 = request.POST.get('password1', None)
           password2 = request.POST.get('password2', None)
           email = request.POST.get('email', None)
           phonenumber = request.POST.get('phonenumber', None)
           nickname = request.POST.get('nickname', None)
           if username=="":
               error=error+"账号不能为空"
               return render(request, myhtml, {'error': error,"loginstr":loginstr})
           if not ( (username.isalpha() or username.isdigit()) and username.isalnum()):
               error = error + " 账号只能是字母和数字"
               return render(request, myhtml, {'error': error,"loginstr":loginstr})
           if nickname=="":
               error = error + " 昵称不能为空"
               return render(request, myhtml, {'error': error,"loginstr":loginstr})

           user =  models.ArticleUserinfor.objects.filter(username=username).first()
           if user:
               print("该用户已存在")
               error="该账号已存在"
               return render(request,myhtml,{'error':error,"loginstr":loginstr})
           if password1=="" or password2=="" :
                error="密码或确认密码不能为空"
                return render(request, myhtml, {'error': error,"loginstr":loginstr})
           if password2 !=password1 :
                error="确认密码与密码不一致"
                return render(request, myhtml, {'error': error,"loginstr":loginstr})
           if not phonenumber:
               phonenumber=None
           models.ArticleUserinfor.objects.create(username=username,password=password1,phone_number=phonenumber,email=email,nickname=nickname,gender=0,desc="你还没介绍你下自己",score=0,imgurl='/static/assets/img/default.jpg')
           re=redirect('/')
           re.set_cookie("username",username)
           return  re
        except :
            error = "出现异常"
            return render(request, myhtml, {'error': error,"loginstr":loginstr})
     return  render(request,myhtml,{"loginstr":loginstr})

def showhtml(request,id):
     loginstr = islogin(request)
     addscore(request, 2)
     userAgent = request.META['HTTP_USER_AGENT']
     print(userAgent)
     if (judge_pc_or_mobile(userAgent)):
         return render(request, 'm'+id + '.html', {"loginstr": loginstr})
     return render(request,id+'.html',{"loginstr":loginstr})
def picedu(request):
    loginstr = islogin(request)
    # result = models.Article.objects.all()
    # article=[]
    # for myre in result:
    #     a={}
    #     a['article_id']=myre.article_id
    #     a['title']=myre.title
    #     a['content']=myre.content
    #     a['type_id']=myre.type_id
    #     a['user_id']=myre.user_id
    #     cache.set('article:'+str(myre.article_id), json.dumps(a))
    # #print(json.loads(cache.get('article:*')))
    # it=cache.keys("article:*")
    # for i in it:
    #     print(i)

    #cache.set('article',json.dumps(article))
    addscore(request, 2)
    userAgent = request.META['HTTP_USER_AGENT']
    #print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'mpicedu.html', {"loginstr": loginstr})
    return  render(request,'picedu.html',{"loginstr":loginstr})
def manbody(request):
    loginstr = islogin(request)
    addscore(request, 2)
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'mmanbody.html', {"loginstr": loginstr})
    return render(request,'manbody.html',{"loginstr":loginstr})
def womanbody(request):
    loginstr = islogin(request)
    addscore(request, 2)
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'mwomanbody.html', {"loginstr": loginstr})
    return render(request,'womenbody.html',{"loginstr":loginstr})
def insert_comment(request):
    addscore(request, 10)
    name = request.COOKIES.get('username')
    response={}
    response['islogin']='True'
    if not name:
        print("空")
        response['islogin']='False'
        response=HttpResponse(json.dumps(response))
        article_id = request.POST.get('article_id', None)
        mycomment = request.POST.get('mycomment', None)
        response.set_cookie('aid', article_id)
        if mycomment !=None:
           response.set_cookie('comment_cookie', json.dumps(mycomment))
        return response
    response['state']=True
    try:
        ##title = request.POST.get('myconment', None)
        mycomment = request.POST.get('mycomment', None)
        article_id=request.POST.get('article_id',None)
        #print(mycomment)

        user = models.ArticleUserinfor.objects.filter(username=name).first()
        models.Comment.objects.create(comment_content=mycomment, article_id=article_id, user_id=user.id)

    except:
        response['state'] = False
    return HttpResponse(json.dumps(response))

def showuser(request):
    loginstr = islogin(request)
    user_id=request.GET.get('user_id', None)
    user = models.ArticleUserinfor.objects.filter(id=user_id).first()
    name = request.COOKIES.get('username')
    me=None
    followlist=[]
    followerlist = []
    #followerlist = []
    followees = []
    followlist = []
    if True:
        if name:
            me = models.ArticleUserinfor.objects.filter(username=name).first()
            follows = models.Follow.objects.filter(follower=me.id)


            for ff in follows:
               followee=models.ArticleUserinfor.objects.filter(id=ff.followee).first()
               ##followees.append(followee)
               followlist.append(ff.followee)
        userfollowees = models.Follow.objects.filter(follower=user_id)
        for   ff in userfollowees:
            followee = models.ArticleUserinfor.objects.filter(id=ff.followee).first()
            followees.append(followee)
        followers = models.Follow.objects.filter(followee=user_id)

        for ff in followers:
            follower = models.ArticleUserinfor.objects.filter(id=ff.follower).first()
            followerlist.append(follower)
    myarticle = models.Article.objects.filter(user_id=user_id)
    sex = ""
    csssex = ""
    if user.gender == 0:
        sex = 'fa fa-mars'
        csssex = "color:blue"
    else:
        sex = 'fa fa-venus'
        csssex = "color:pink"
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'muser.html',  {'user': user, "me": me, "followeelist": followees, "followerlist": followerlist,"followId_list": followlist, "me": me, 'myarticle': myarticle, 'imgurl': user.imgurl, "sex": sex,
                       "csssex": csssex, "loginstr": loginstr})

    return render(request, 'user.html', {'user': user,"me":me,"followeelist":followees,"followerlist":followerlist,"followId_list":followlist,"me":me, 'myarticle': myarticle,'imgurl':user.imgurl,"sex":sex,"csssex":csssex,"loginstr":loginstr})

def zhan(request):
    name = request.COOKIES.get('username')
    response = {'state': True}
    response['islogin'] = 'True'
    if not name:
        response['islogin'] = 'False'
        myresponse = HttpResponse(json.dumps(response))
        article_id = request.POST.get('article_id', None)
        #mycomment = request.POST.get('mycomment', None)
        #print(article_id+"id")
        myresponse.set_cookie('aid', article_id)

        return myresponse
    try:
        article_id = request.POST.get('article_id', None)
        add = request.POST.get('add', None)
        user = models.ArticleUserinfor.objects.filter(username=name).first()
        myarticle=models.Article.objects.filter(article_id=article_id).first()
        count=int(myarticle.supportcount)
        if(add=="1"):
            count = count + 1
            models.Article.objects.filter(article_id=article_id).update(supportcount=count)
            models.Support.objects.create(user_id=user.id,article_id=article_id)
        else:
            count=count-1
            models.Article.objects.filter(article_id=article_id).update(supportcount=count)
            models.Support.objects.filter(user_id=user.id,article_id=article_id).delete()
        #models.Article.objects.filter(article_id=article_id).update(supportcount=count)
        response['count']=str(count)
        print(user.username)
    except:
        response['state'] = False

    return   HttpResponse(json.dumps(response))

# def create_alipay():
#     ali_pay = AliPay(
#         appid=settings.ALIPAY_APPID,
#         app_notify_url=None,
#         app_private_key_path=os.path.join(settings.BASE_DIR, 'static\\s2048.txt'),
#         alipay_public_key_path=os.path.join(settings.BASE_DIR, 'static\\g2048.txt'),
#         sign_type='RSA2',
#         debug=True)
#     return ali_pay
#
#
#
# def get_alipay_page():
#     ali_pay = AliPay(
#         appid=settings.ALIPAY_APPID,
#         app_notify_url=None,
#         app_private_key_path=os.path.join(settings.BASE_DIR, 'static\\s2048.txt'),
#         alipay_public_key_path=os.path.join(settings.BASE_DIR, 'static\\g2048.txt'),
#         sign_type='RSA2',
#         debug=True)
#     order_string = ali_pay.api_alipay_trade_page_pay(
#         out_trade_no="20161112123",
#         total_amount=0.01,
#         subject="计科162王狗蛋的狗头",
#         #return_url="http://",
#         #notify_url="https://openapi.alipay.com/gateway.do"  # this is optional
#     )
#
#     print(order_string)
#     return settings.ALIPAY_URL + order_string
#
#
#
#
# def get_alipay_query(order_id):
#      """查询订单状态"""
#      alipay = create_alipay()
#      result = alipay.api_alipay_trade_query(out_trade_no=order_id)
#      print(result)
#      if result.get("trade_status", "") == "TRADE_SUCCESS":
#           return True
#      else:
#        return False
#
#
# def zhifu(request):
#     u=get_alipay_page()
#     return redirect(u)


def gettip(request):
    key=request.POST.get("key",None)
    response = {'state': True}
    st=""
    if  key :
        result = models.Article.objects.raw("select distinct * from article where title like '%%"+key+"%%'")
        for rr in result:
            st=st+rr.title+"//"
    else :
       pass
    response['result']=st
    print(key)
    return HttpResponse(json.dumps(response))

def modify(request):
    loginstr = islogin(request)
    mesg=""
    if request.method=="POST":
        name = request.COOKIES.get('username')
        if not name:
            userAgent = request.META['HTTP_USER_AGENT']
            # print(userAgent)
            if (judge_pc_or_mobile(userAgent)):
                return render(request, "mpleaselogin.html", {"loginstr": loginstr})
            return render(request,"pleaselogin.html",{"loginstr":loginstr})
        try:
              user = models.ArticleUserinfor.objects.filter(username=name).first()
              nickname= request.POST.get("nickname")
              if nickname!="":
                  #print("提交了昵称")
                  models.ArticleUserinfor.objects.filter(id=user.id).update( nickname=nickname)
                  mesg =mesg+ "昵称修改成功 "
              else:
                  pass
              gender = request.POST.get("gender")
              if gender!="":
                  # print("提交了昵称")
                  models.ArticleUserinfor.objects.filter(id=user.id).update(gender=gender)
                  mesg = mesg+"性别修改成功 "
              else:
                  pass
              desc = request.POST.get("desc")
              if desc!="":
                  # print("提交了昵称")
                  models.ArticleUserinfor.objects.filter(id=user.id).update(desc=desc)
                  mesg = mesg + "简介修改成功 "
              else:
                  pass
              f = request.FILES.get("head")
              if  f:

                 filename = f.name
                 last = filename.split('.')[-1]
                 filepath = os.path.join("/project/sexeducation/collect_static/headimg/", str(user.id)+ "."+last)
                 loadfile = open(filepath, mode="wb")
                 for fi in f.chunks():
                    loadfile.write(fi)
                 loadfile.close()
                 mesg = mesg+"头像修改成功"
                 models.ArticleUserinfor.objects.filter(id=user.id).update(imgurl="/static/headimg/"+str(user.id)+ "."+last)
        except:
              mesg = "修改失败"
        addscore(request, 15)
        return  redirect("/userinfor")
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, "mmodify.html", {"isupload": mesg, "loginstr": loginstr})

    return render(request,"modify.html",{"isupload":mesg,"loginstr":loginstr})


def exit_login(request):
    name = request.COOKIES.get('username')
    if not name:
        return redirect('/')
    else:
        res1 = redirect('/')
        res1.set_cookie('username', "")
        return res1
def sendmessage(request):
       loginstr = islogin(request)
       userAgent = request.META['HTTP_USER_AGENT']

       if (judge_pc_or_mobile(userAgent)):
           return render(request, "msendtomanager.html", {"loginstr": loginstr})

       return render(request, "sendtomanager.html",{"loginstr":loginstr})

def insert_message(request):
    name = request.COOKIES.get('username')
    response = {'state': True}
    try:
        content = request.POST.get('content', None)
        if name:
            user = models.ArticleUserinfor.objects.filter(username=name).first()
            print("user.id",user.id)
            models.Message.objects.create(content=content,userid=user.id)
            print("插入成功")
        else:
            models.Message.objects.create(content=content)
        #print(title)
    except:
        response['state'] = False
    return HttpResponse(json.dumps(response))
def managerlogin(request):
    msg = {}
    error = ""
    msg['username'] = ""
    msg['password'] = ""
    if(request.method == 'GET'):
        return render(request,"managerlogin.html",{'error': error, 'msg': msg})
    if (request.method == 'POST'):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username == "" or password == "":
            error = "账号密码不能为空"
            return render(request, "managerlogin.html", {'error': error, 'msg': msg})
        else:
            user = models.Manager.objects.filter(username=username).first()
            if not user:
                error = "该用户不存在"
                return render(request, "managerlogin.html", {'error': error, 'msg': msg})

            if user.password == password:
                res = redirect('/manageruserinfor/')
                res.set_cookie('manageusername', username)
                return res
            error = "密码错误"
            return render(request, "managerlogin.html", {'error': error, 'msg': msg})

def manageruserinfor(request):
     name = request.COOKIES.get('manageusername')
     if not name:
        return redirect('/managerlogin/')
     message= models.Message.objects.all()
     mymessage=[]
     for cc in message:
         comment_tamp = {}
         if cc.userid:
             user = models.ArticleUserinfor.objects.filter(id=cc.userid).first()

             comment_tamp["username"] = user.username
             comment_tamp["user_id"] = user.id
             comment_tamp["content"] = cc.content
             comment_tamp["nickname"] = user.nickname
             comment_tamp["message_id"] = cc.id
             mymessage.append(comment_tamp)

         else:
             print("userid为空")
             comment_tamp["content"] = cc.content
             comment_tamp["nickname"] = "匿名用户"
             comment_tamp["message_id"] = cc.id
             mymessage.append(comment_tamp)
     return   render(request,"managerinfor.html",{"mymessage":mymessage})
def message(request):
    id=request.GET.get("id",None)
    mes = models.Message.objects.filter(id=id).first()
    return  render(request,"showmessage.html",{"content":mes.content})

def sendto(request):
    if  request.method=="GET":
         to_userid=request.GET.get("id",None)
         from_name=request.COOKIES.get('username')
         if  from_name :
                user = models.ArticleUserinfor.objects.filter(username=from_name).first()
                user2 = models.ArticleUserinfor.objects.filter(id=to_userid).first()
                from_id=user.id
                return  render(request,"sendto.html",{"from_id":from_id,"to_id":to_userid,"tonickname":user2.nickname})
         else:
                return  redirect("/login")
    from_name = request.COOKIES.get('username')
    if request.method=="POST":
      response = {'state': True}
      if from_name:
        #response = {'state': True}
        response['islogin']=True
        try:
            user = models.ArticleUserinfor.objects.filter(username=from_name).first()
            content = request.POST.get("content", None)
            from_id = user.id
            to_id = request.POST.get("to_id", None)
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
            models.Usermessage.objects.create(content=content,from_id=from_id,to_id=to_id,time=nowTime)

            # print(title)
        except:
            response['state'] = False
        return HttpResponse(json.dumps(response))
      else :
          response['islogin'] = False
          return HttpResponse(json.dumps(response))


def mymessage(request):
    loginstr = islogin(request)
    name = request.COOKIES.get('username')
    if not name:
        userAgent = request.META['HTTP_USER_AGENT']
        # print(userAgent)
        if (judge_pc_or_mobile(userAgent)):
            return render(request, "mpleaselogin.html", {"loginstr": loginstr})
        return render(request,"pleaselogin.html",{"loginstr":loginstr})
    user=models.ArticleUserinfor.objects.filter(username=name).first()
    message = models.Usermessage.objects.filter(Q(to_id=user.id )|Q(from_id=user.id)).order_by('-time')
    mymessage = []
    for cc in message:
        comment_tamp = {}

        user3 = models.ArticleUserinfor.objects.filter(id=cc.from_id).first()
        user4= models.ArticleUserinfor.objects.filter(id=cc.to_id).first()
        #comment_tamp["myusername"] = user.username
        comment_tamp["myuser_id"] = user.id
        comment_tamp["content"] = cc.content
        comment_tamp["mynickname"] = user.nickname
        comment_tamp["message_id"] = cc.id
        comment_tamp["from_nickname"] = user3.nickname
        comment_tamp["from_id"] = user3.id
        comment_tamp["to_id"]=cc.to_id
        comment_tamp["to_nickname"] = user4.nickname
        comment_tamp["time"] = cc.time
        comment_tamp["from_img"] = user3.imgurl
        mymessage.append(comment_tamp)
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, "mmymessage.html",{"mymessage": mymessage, "mynickname": user.nickname, "myimg": user.imgurl, "user": user,
                       "loginstr": loginstr})

    return render(request, "mymessage.html", {"mymessage": mymessage,"mynickname":user.nickname,"myimg":user.imgurl,"user":user,"loginstr":loginstr})

def usermessage(request):
    loginstr = islogin(request)
    id=request.GET.get("id",None)
    message = models.Usermessage.objects.filter(id=id).first()
    return  render(request,"showusermessage.html",{"content":message.content,"loginstr":loginstr})

def testedit(request):
    return render(request,"edittest.html")
def  upload_img(request):
    files = request.FILES.get("imgFile", None)
    print(files.name)
    filename=files.name
    t = time.time()
    last=filename.split('.')[1]
    picname=str(int(round(t * 1000)))+"."+last
    filepath="/project/sexeducation/collect_static/image/" + picname
    loadfile = open(filepath, mode="wb")
    for fi in files.chunks():
        loadfile.write(fi)
    loadfile.close()
    result = {"error": 0, "url": "/static/image/"+picname}
    return  HttpResponse(json.dumps(result), content_type="application/json")


def follow(request):
    follower_id=request.POST.get("follower_id",None)
    followee_id = request.POST.get("followee_id",None)
    follow_tip=request.POST.get("follow_tip",None)

    if  follow_tip=="ok":
         models.Follow.objects.create(follower=follower_id,followee=followee_id)
         return HttpResponse("focused")
    if   follow_tip=="cancel":
        models.Follow.objects.filter(follower=follower_id,followee=followee_id).first().delete()
        return HttpResponse("canceled")
def video_play(request):
    loginstate="1"
    name = request.COOKIES.get('username')
    if not name:
        loginstate="0"
    loginstr = islogin(request)
    vid = request.GET.get("id", None)
    video = models.Videolist.objects.filter(id=vid).first()
    seenum=int(video.seenum)
    seenum=seenum+1
    models.Videolist.objects.filter(id=vid).update(seenum=seenum)
    comment = []
    mycommtent = models.Vcomment.objects.filter(vid=vid)
    for cc in mycommtent:
        user=models.ArticleUserinfor.objects.filter(id=cc.userid).first()
        comment_tamp={}
        comment_tamp["username"]=user.username
        comment_tamp["user_id"]=user.id
        comment_tamp["comment_content"]=cc.mycomment
        comment_tamp["nickname"]=user.nickname
        comment_tamp["ctime"] = cc.ctime
        comment.append(comment_tamp)
    dmlist=models.Danmu.objects.filter(vid=vid)
    mydm=[]
    for dm in dmlist:
        dmtamp={}
        dmtamp["text"]=dm.content
        dmtamp["size"]=int(dm.dsize)
        dmtamp["color"]=dm.color
        dmtamp["time"]=int(dm.dtime)*10
        dmtamp["position"]=int(dm.position)
        mydm.append(dmtamp)
    dmresult=json.dumps(mydm, ensure_ascii=False)
    print(dmresult)
    userAgent = request.META['HTTP_USER_AGENT']
    print(userAgent)

    if (judge_qq_mobile(userAgent)):
       #print("111212212212")

       return render(request,'playvideomobile.html',{"video":video,"loginstr":loginstr,"comment":comment,"vid":vid,"loginstate":loginstate,"dmresult":str(dmresult)})

    if (judge_pc_or_mobile(userAgent)):
        return render(request,'mplayvideo.html',{"video":video,"loginstr":loginstr,"comment":comment,"vid":vid,"loginstate":loginstate,"dmresult":str(dmresult)})

    return render(request,'playvideo.html',{"video":video,"loginstr":loginstr,"comment":comment,"vid":vid,"loginstate":loginstate,"dmresult":str(dmresult)})

def video_list(request):
    loginstr = islogin(request)
    typevid= request.GET.get("tp", 0)
    # result = models.Videolist.objects.all()
    addscore(request, 2)
    # cache.set("name","陈永喆")
    # myname=cache.get("name")
    # print(myname)
    result=None
    if typevid==0 or typevid=="0":
        result = models.Videolist.objects.all()
    else:
       result= models.Videolist.objects.filter(videotp=typevid)
    count = len(result)
    num = "总共" + str(count) + "个视频"
    current_page = request.GET.get("p", 1)
    print(current_page)
    current_page = int(current_page)
    start = (current_page - 1) * 8
    end = current_page * 8
    ##print(result[1].title)
    #result.reverse()
    ##print(result[1].title)
    #data1 = result[count - end-1:count - start-1]
    result1=list(result)
    result1.reverse()
    data=result1[start:end]
    #print(data)
    #data = list(data)
    #data.reverse()
    #print(data)
    ##print(data[1].title)
    all_count = count
    total_count, y = divmod(all_count, 8)
    if y:
        total_count += 1
    page_list = []
    nav = """<nav aria-label= "Page navigation" >
            <ul class ="pagination" >"""
    page_list.append(nav)
    page_num = 7
    start_index = 1
    end_index = 0
    if total_count < page_num:
        start_index = 1
        end_index = total_count + 1
    else:
        if current_page <= ((page_num + 1) / 2):
            start_index = 1
            end_index = page_num + 1
        else:
            start_index = current_page - (page_num - 1) / 2
            end_index = current_page + (page_num + 1) / 2
            if (current_page + (page_num - 1) / 2) > total_count:
                end_index = total_count + 1
                start_index = total_count - page_num + 1
    pre = ""
    if current_page == 1:
        pre = """<li>
                <a href="#" aria-label = "Previous" >
                <span aria-hidden = "true" > &laquo; </span></a>
               </li>"""

        # pre = '<a class="page" href="#">上一页</a>'
    else:
        pre = '<li>  <a href = "/videolist'
        pre2 = """?p=%s" aria-label="Previous" >
                       <span aria-hidden="true" > &laquo; </span></a>
                      </li>""" % (current_page - 1)
        pre = pre + pre2
        #        print(pre)
    page_list.append(pre)

    for i in range(int(start_index), int(end_index)):
        if i == current_page:
            temp = '<li class ="active" > <a href="/videolist?&p=%s&tp=%s">%s</a></li>' % (i,typevid, i)
            # temp = '<a class="page isactive" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
        else:
            # temp = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">%s</a>' % (i, i)
            temp = '<li> <a href="/videolist?p=%s&tp=%s">%s</a></li>' % (i,typevid, i)
        page_list.append(temp)
    afterpage = ""
    if current_page == total_count:
        # afterpage = '<a class="page" href="#">下一页</a>'
        afterpage = """<li>
                        <a href="#" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span></a>
                       </li>"""
    else:
        afterpage = '<li>  <a href = "/videolist?'
        afterpage2 = """p=%s" aria-label="Next" >
                               <span aria-hidden ="true">&raquo;</span></a>
                              </li>""" % (current_page + 1)
        afterpage = afterpage + afterpage2
        # afterpage = '<a class="page" href="/s/?keyword='+keyword+'&p=%s">下一页</a>' % (current_page + 1)
        page_list.append(afterpage)
    nav2 = '</ul> </nav>'
    page_list.append(nav2)
    page_str = "".join(page_list)
    # for i in range(len(data)):
    #     data[i].content = re.sub("[A-Za-z0-9\!\%\[\]\,\。<>/\"=-_.-: ;]", "", data[i].content)
    #     data[i].content = data[i].content[0:90]
    userAgent = request.META['HTTP_USER_AGENT']
    # print(userAgent)
    if (judge_pc_or_mobile(userAgent)):
        return render(request, 'mvideolist.html',
                      {'videolist': data, 'num': num, 'page_str': page_str, "loginstr": loginstr})

    return render(request, 'videolist.html', {'videolist': data, 'num': num, 'page_str': page_str,"loginstr":loginstr})


def insert_vcomment(request):
    addscore(request, 10)
    name = request.COOKIES.get('username')
    response={}
    response['islogin']='True'
    if not name:
        loginstr = islogin(request)
        return render(request,"pleaselogin.html",{"loginstr":loginstr})
    response['state']=True
    try:
        ##title = request.POST.get('myconment', None)
        mycomment = request.POST.get('mycomment', None)
        vid=request.POST.get('vid',None)
        #print(mycomment)
        ctime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        user = models.ArticleUserinfor.objects.filter(username=name).first()
        models.Vcomment.objects.create(mycomment=mycomment, vid=vid, userid=user.id,ctime=ctime)

    except:
        response['state'] = False
    return HttpResponse(json.dumps(response))

def insert_dm(request):
    vid=request.POST.get('vid', None)
    dsize = request.POST.get('dsize', None)
    content= request.POST.get('content', None)
    color = request.POST.get('color', None)
    if color=='white':
        color='#FFFFFF'
    if color=="red":
        color="#FF0000"
    if color=='green':
        color="#008000"
    if color=="blue":
        color="#00BFFF"
    if color=="yellow":
        color="#FFFF00"
    position=request.POST.get('position', None)
    mytime=request.POST.get('mytime', None)
    models.Danmu.objects.create(content=content, vid=vid, position=position, dtime=(int(mytime)/10),color=color,dsize=dsize)
    return HttpResponse('true')


def insert_dm1(request):
    vid=request.POST.get('vid', None)
    dsize = request.POST.get('dsize', None)
    content= request.POST.get('content', None)
    color = request.POST.get('color', None)
    position=request.POST.get('position', None)
    mytime=request.POST.get('mytime', None)
    models.Danmu.objects.create(content=content, vid=vid, position=position, dtime=mytime,color=color,dsize=dsize)


def get_dm(request):

    if request.method=="POST":


        #postBody=  request.body
        #postBody.decode('utf-8')
        json_result = json.loads(request.body.decode('utf-8'))
        vid = json_result['id']
        #print(json_result['color'])
        #dsize = request.POST.get('dsize', None)
        content = json_result['text']
        # print(content)
        color =json_result['color']
        coloroc=hex(color)
        color='#'+str(coloroc[2:])
        position = json_result['type']
        mytime =int(json_result['time'])
        models.Danmu.objects.create(content=content, vid=vid, position=position, dtime=mytime, color=color, dsize=0)
        r = {"code": 0}

        return JsonResponse(r,json_dumps_params={'ensure_ascii':False})
    if request.method=="GET":
        vid=request.GET.get('id', None)
        dmlist = models.Danmu.objects.filter(vid=vid)
        mydm = {}
        mydm["code"]=0;
        dml=[]
        for dm in dmlist:
            dmtamp=[]
            dmtamp.append(dm.dtime)
            dmtamp.append(int(dm.position))
            coloroc=dm.color[1:]
            color=int(coloroc,16)
            dmtamp.append(color)
            dmtamp.append("用户")
            dmtamp.append(dm.content)
            dml.append(dmtamp)
        mydm["data"]=dml

        # r={"code": 0, "data": [[113.001021,0,16777215,"DIYgod", "这不是赤祼祼打大幂幂脸吗？比她唱的好那么多"],[0,1,15024726,"DIYgod","HAHAHA"]]}
        # rr={"code":0,"data":[[113.001021,0,16777215,"DIYgod","333333333333333333333333333333"],[137.31192,0,16777215,"DIYgod","srtdhgfdghdrtdd uytdfj"],[220.5405441,0,16777215,"DIYgod","哈哈啊哈"],[29.43929,0,16777215,"DIYgod","得得得"],[7.556685,0,16777215,"DIYgod","666"],[15.836185,0,16777215,"DIYgod","999999999999999999999999999999"],[0,0,16777215,"DIYgod","???"],[25.000842,0,16777215,"DIYgod","sdfsdfsdaf"],[30.243957,0,16777215,"DIYgod","wqqwrwer"],[9.136597,0,15024726,"DIYgod","fadsfsdafsdafsd"],[0.054,0,16777215,"DIYgod","6666"],[7.361067,0,16777215,"DIYgod","1591951"],[10.902319,0,16777215,"DIYgod","591951"],[17.647142,0,16777215,"DIYgod","瞎操心"],[21.41331,0,16777215,"DIYgod","踩踩踩"],[6.093356,0,16777215,"DIYgod","0."],[403.20676,0,16777215,"DIYgod","haha"],[4.954906,0,16777215,"DIYgod","嗯嗯"],[24.077292,1,13959417,"DIYgod","。。。。。。。。。。"],[0,1,15024726,"DIYgod","HAHAHA"],[5.493229,0,16777215,"DIYgod","55555"],[8.783629,0,16777215,"DIYgod","哈哈哈"],[0.054,0,16777215,"DIYgod","更好让他"],[10.045058,0,16777215,"DIYgod","给别人突然"],[24.88538,0,16769331,"DIYgod","个人男人女人"],[4.193995,0,16777215,"DIYgod","gfgf"],[10.394029,0,16777215,"DIYgod","给你"],[8.959122,0,16777215,"DIYgod","的深V"],[17.510375,0,16777215,"DIYgod","是多方播放"],[44.798186,0,16777215,"DIYgod","仿贝多芬"],[97.436834,0,16777215,"DIYgod","aaaa"],[11.892745,0,16777215,"DIYgod","gdgdgd"],[36.857279,0,16777215,"DIYgod","xxcvcxvxvxvxvxvxxvxvx"],[45.562938,0,16777215,"DIYgod","x xc x x"],[153.103135,0,16777215,"DIYgod","123"],[6.120641,0,16777215,"DIYgod","gggghkjkjkjkj"],[28.563801,0,16777215,"DIYgod","46465465"],[16.095017,0,16777215,"DIYgod","dsdsd"],[16.518226,0,16777215,"DIYgod","dsdsd"],[16.853606,0,16777215,"DIYgod","dsdsd"],[17.019411,0,16777215,"DIYgod","dsdsd"],[141.136573,0,16777215,"DIYgod","我去"],[17.174086,0,16777215,"DIYgod","546"],[116.792532,0,16777215,"DIYgod","56"]]}
        # ##rrr={"code":0,"data":[[0,2,15024726,"DIYgod","HAHAHA"],[114.958,0,16777215,"f6addbf1","这不是赤祼祼打大幂幂脸吗？比她唱的好那么多"],[324.417,0,16777215,"f6addbf1","不亏是我的女神"],[20.321,0,16777215,"2160aef0","没人？"],[282.157,0,16777215,"3fd69c7a","好"],[64.943,0,0,"7c2dd6fc","还是杨钰莹唱的好"],[250.016,0,0,"4610f251","真甜呐唱的"],[137.301,1,16777215,"d4377592","这首歌好听"],[164.949,1,16777215,"d4377592","好漂亮"],[232.618,1,16777215,"d4377592","这衣服很气质"],[292.096,1,16777215,"d4377592","比年轻时还有味道"],[257.877,0,16777215,"d4377592","娇小可爱型"],[28.068,0,16777215,"b11e47e6","bgm 爱的供养  再问自杀"],[199.679,0,16777215,"44ab5f3d","一样的你"],[35.306,1,14811775,"480c1629","女神没有之一"],[23.755,0,16777215,"77bb9627","好听哭"],[237.38,0,16777215,"77bb9627","女神唱歌真是秒杀啊  太美了"],[370.832,0,16777215,"77bb9627","救命啊太好听了"],[12.652,0,16777215,"d93eb39c","听过最好的版本没有之一"],[69.1,0,16777215,"1c19471a","好棒"],[305.147,0,16777215,"1c19471a","不能再棒啦"],[22.872,0,16777215,"165b1d35","有呀"],[39.864,0,16777215,"165b1d35","红的别走"],[105.871,0,0,"6f42f177","我居然在b站听爱的自杀。。。"],[379.908,0,16777215,"165b1d35","不管(;｀O´)o自己跑"],[116.276,0,16777215,"1ce206d0","以前的歌星可是实力派"],[269.173,0,16777215,"1ce206d0","她以前和毛宁可是称为金童玉女啊，歌美人甜不是吹的"],[283.992,0,16777215,"9372442d","真的超好听"],[56.698,0,16777215,"46b59d89","这声线真是 好听死了"],[25.822,0,0,"326a24bf","BGM 爱的自杀 再问供养"],[180.676,1,15138834,"326a24bf","↙曾贤儿"],[120.399,0,16777215,"225adcfd","其实吧，是个歌手唱都会打她脸的吧。。。"],[278.989,0,16777215,"225adcfd","是歌甜人美"],[1.306,0,16777215,"b44c7fb3","唱法跟以前不同喽，气息不够用了，岁月无情啊。。。 "],[29.565,0,0,"db1c5ec9","老了"],[29.519,0,16777215,"b6ba9676","老了"],[62.507,0,16777215,"7f7d4f28","喔，好听"],[221.691,0,16777215,"d1852686","啊啊啊一帘幽梦"],[39.532,0,16777215,"674fb07c","最好听的一版"],[39.585,0,16777215,"1f860d38","岁月催人老啊"],[259.321,0,16777215,"3a898846","好喜欢"],[27.3,0,16777215,"75b44204","哎呀杨幂在现场么"],[329.039,0,16777215,"163b0ea5","宝刀未老"],[222.805,2,16777215,"950a873b","杨导演：钰莹，这歌唱完第一段脱掉衣服。"],[373.212,0,16777215,"52323868","承包中石叔"],[39.638,0,16777215,"d0f8763b","空耳君呢？"],[113.741,0,16777215,"a0e6bd1d","太美了"],[49.361,0,41194,"6de544c6","啊，此处承包我家诗诗，龙葵蓝"],[133.322,0,16777215,"4de11e12","我不想说，每次听到她唱歌，都很开心"],[168.682,0,16777215,"4de11e12","声音怎么那么好听"],[249.522,0,16777215,"4de11e12","声音好听，长的也很漂亮"],[276.362,0,16777215,"4de11e12","我要是找老婆就要找这样的"],[337.828,0,16777215,"5866f752","她的专辑销量至今没几个女歌手超过的"],[380.411,0,0,"c4fd44d5","甜歌天后啊"],[256.372,0,16777215,"43c0ff38","全程微笑"],[5.935,0,13369344,"89370ab2","啦啦啦"],[37.816,0,0,"f5025512","原来这歌没问题"],[60.701,0,0,"f5025512","吴奇隆星星眼"],[69.782,0,0,"47f6a970","果然歌也是要分人唱的"],[304.274,0,0,"47f6a970","周迅"],[140.638,0,16777215,"4de11e12","很喜欢她"],[151.578,0,16777215,"4de11e12","好想娶她"],[271.7,0,16777215,"166909c0","前面说假唱的是说谁？这个明显是真唱而且唱的很好"],[200.012,0,16777215,"a5c878a0","人的经历和沧桑都会从眼睛里透出来"],[147.3,0,16777215,"8c78ff94","底下坐的很多人可以说听这首歌长大的吧..."],[32.425,0,16777215,"82a32ddd","谁敢说，女神老了"],[65.321,0,16777215,"82a32ddd","羞煞一票当代明星"],[133.609,0,16777215,"82a32ddd","原汁原味"],[31.259,0,0,"c7e8dae0","我幂14年不在现场"],[195.949,0,16777215,"4ea72cae","好美"],[189.425,0,16777215,"42764996","外来妹"],[235.803,0,16777215,"1a8699ed","超喜欢这个一帘幽梦"],[42.777,0,16777215,"a5c878a0","眼睛会说话哦"],[44.184,0,16777215,"a5c878a0","眼睛会说话"],[230.738,0,16777215,"cf2a9ca2","被这首炸出来"],[12.918,0,16777215,"b13b06ab","好听"],[248.711,0,16777215,"6e850cbc","随时变调切唱腔。唱功真好。"],[342.198,0,16777215,"6e850cbc","周迅那个公鸭嗓跟甜歌妹子哪里一样了 "],[375.092,0,16777215,"6e850cbc","最火的时候淡出了几年，否则有那英王菲什么事"],[352.737,0,16777215,"5fa61fa8","这才是骨头都化了"],[21.772,0,16777215,"5fa61fa8","这就叫做味道"],[148.902,0,16777215,"db7fb6f8","好美"],[151.802,0,16777215,"db7fb6f8","爱岗岗"],[245.598,0,0,"b3f783a4","笑得真美"],[47.359,0,16777215,"165d0afe","别的不说，她是那种嗓子就应该去唱歌的人啊"],[219.594,0,16777215,"14dc43c","66666"],[256.936,0,16777215,"14dc43c","不愧是女神"],[318.767,0,0,"dd47ecb0","底下的人一脸享受"],[367.591,0,0,"dd47ecb0","这歌特别显音色"],[357.637,0,0,"dd47ecb0","要是当年没有赖家的事情，她现在绝不会混成这样不上不下的样子"],[268.26,0,16777215,"3914c849","爱岗岗"],[122.486,0,0,"548370d9","真的好听"],[320.552,0,0,"12e5a9a6","她的咖位还需要假唱？笑死"],[381.752,0,0,"12e5a9a6","她可是大陆第一个明星"],[400.8,0,0,"12e5a9a6","ps，解放后"],[385.14,0,16777215,"8770a34e","还是以前的歌手唱功好，随随便便摔那些选秀歌手18条街。"],[198.94,0,16777215,"bbdc7b1","当年还是甜姑娘，和现在的真的唱出了不同，这才是真正的歌手"],[339.59,0,16777215,"1495591b","这版月圆花好超赞啊"],[375.103,0,16777215,"1495591b","有没有单独这一首啊"],[345.89,0,16777215,"bbdc7b1","戏中演员明显听醉了"],[26.655,0,16777215,"f895d25b","以前都是这种字正腔圆的纯正唱法"],[30.591,0,16777215,"d320f48","这首歌原来这么好听啊"],[53.498,0,16777215,"d320f48","比我大20岁，比我还年轻"],[268.173,0,16777215,"d320f48","好听的我快哭了"],[223.059,0,16777215,"51380f25","6666"],[21.479,0,16777215,"5c4ce08","实力那么好还那么漂亮"],[234.719,0,16777215,"5c4ce08","这首歌真心好听"],[282.444,0,16777215,"5c4ce08","她不过不会做饭哈哈哈"],[256.06,0,16777215,"65b65c3d","这歌原唱挺忧郁的，给她唱的魅惑死了"],[14.901,0,16777215,"3342ebf","啊啊啊啊啊啊啊啊啊太好听了"],[14.901,0,14811775,"3342ebf","啊啊啊啊啊啊啊啊啊太好听了"],[14.901,0,9487136,"3342ebf","啊啊啊啊啊啊啊啊啊太好听了"],[14.901,0,15772458,"3342ebf","啊啊啊啊啊啊啊啊啊太好听了"],[14.901,0,11890,"3342ebf","啊啊啊啊啊啊啊啊啊太好听了"],[14.901,0,15138834,"3342ebf","啊啊啊啊啊啊啊啊啊 太好听了"],[138.976,0,15138834,"3342ebf","她唱什么都好听"],[155.317,0,15138834,"3342ebf","想娶+1，本人女，莹火虫，梦想就是娶她"],[199.392,0,16707842,"3342ebf","好美，舔屏"],[263.52,0,16707842,"3342ebf","好可爱"],[357.941,0,16707842,"3342ebf","全身酥"],[40.015,0,0,"83968663","岗岗我爱你"],[79.651,0,0,"83968663","岗岗我爱你"],[142.172,0,0,"83968663","岗岗我爱你"],[166.048,0,0,"83968663","岗岗我爱你"],[248.561,0,0,"83968663","没脱啊？死阿婆主"],[280.929,0,0,"83968663","岗岗我爱你"],[312.382,0,0,"83968663","岗岗我爱你"],[343.632,0,0,"83968663","应该换个造型"],[367.286,0,0,"83968663","把导演拖出去打"],[330.147,0,16777215,"65b65c3d","女神唱儿歌"],[334.347,0,16777215,"65b65c3d","女神唱儿歌挺好听的，是能把儿歌唱出花来那种"],[351.745,0,16777215,"5c638c5b","唱的真好听"],[158.33,0,16777215,"8c78ff94","刚刚不就是汤镇业吗"],[64.308,0,16777215,"d3c2da76","终于不是乳腺癌和肺癌了"],[238.133,0,16777215,"95fe8ca6","陈数小姐姐"],[137.287,0,13408767,"a75faa8c","太赞了"],[175.629,0,16777215,"9cc507c1","汤镇业是外来妹的男一号"],[192.725,0,16777215,"9cc507c1","汤镇宗好不啦"],[291.958,0,16777215,"153af7d9","说假唱的估计00后。。"],[263.688,0,16777215,"3752c063","太美太美了"],[116.612,0,16777215,"7b9d67b5","醉倒温柔乡"],[195.067,0,16777215,"7b9d67b5","还是一样的你"],[201.843,0,16777215,"7b9d67b5","还是爱你的我"],[238.587,0,16777215,"7b9d67b5","与我 与我！！！"],[283.9,0,16777215,"7b9d67b5","假唱的 你过来 看我不打死你"],[322.993,0,16777215,"7b9d67b5","说假唱的就没听过杨钰莹的声音"],[375.66,0,16777215,"7b9d67b5","救命啊"],[400.388,0,16777215,"7b9d67b5","谁来救我啊 陷温柔乡里了··"],[54.101,0,16777215,"b7b514ca","小智！nnnnn"],[121.95,0,16777215,"ae85f2f2","别说打大幂幂脸，打现在哪个歌手/明星都够了"],[305.097,0,16777215,"ebe0a2fd","毕竟嗓子不是巅峰，半开麦又尴尬"],[53.145,0,16777215,"dfb6347b","表白此处一闪而过的颖宝，表白钰莹姐"],[217.375,0,16777215,"4649d0fc","啊啊啊啊啊啊啊啊"],[226.072,0,16777215,"71001a0","静静听(⊙_⊙)"],[107.511,0,16777215,"1e647192","这首歌能唱这么好听真是难得了"],[82.934,0,16777215,"a4b884f0","唱的很有感情"],[73.14,0,16777215,"716a63d1","脸上抹的什么玩意儿？金色的！"],[250.248,0,16777215,"db560cbf","杨钰莹歌毛宁的歌都特别的难唱，能唱断气"],[34.252,0,16737792,"c680231a","遥不可及的女神 笔芯"],[141.853,0,0,"ec31a203","看看当年演这部戏滴人都老了，只有岗岗还是当年的风采"],[129.516,0,16777215,"87fe0a6a","好听啊"],[200.391,0,16777215,"87fe0a6a","好听啊"],[82.889,0,16777215,"42c86a9c","高光"],[193.799,0,16777215,"4a9534e4","一点皱纹都没有"],[374.598,0,16777215,"59686280","浑身骨头一苏"],[233.302,0,16777215,"9d2fcc03","哇，，炸出来"],[234.3,0,16777215,"9d2fcc03","童年"],[304.308,2,11890,"9d2fcc03","偷偷表白周公子"],[123.455,0,16777215,"f49c35e1","看到钟汉良"],[51.706,0,16777215,"2144fe63","视频压制后音频会错位 不压不能上传"],[92.561,0,16777215,"46efa8d3","人美歌甜"],[217.233,0,16777215,"46efa8d3","眼镜好好看啊"],[193.225,0,16777215,"22f8345","岗岗风采依旧"],[144.536,0,16777215,"22f8345","岗岗茶山情歌美到了巅峰"],[357.707,0,16777215,"22f8345","底下一众星，听的很享受"],[226.202,0,16777215,"18c53b7c","这么多年了，依然唱的这么好听，不愧为我儿时的女神"],[295.022,0,16777215,"c8a83968","听着就很舒服 都是笑着听完的哈哈"],[298.1,0,16777215,"18c53b7c","00后懂个毛，这是80后和95前这批人的童年儿时女神"],[386.983,0,16777215,"118447eb","表白社长"],[134.16,0,16777215,"6c6db5cd","哇，这首歌和电视剧当年好红"],[100.913,0,16777215,"55b910c0","这可真是温柔乡啊。。。这句最好听"],[78.06,0,0,"ec730332","歌也分谁唱"],[133.703,0,0,"ec730332","多了更多的从容"],[19.029,0,16777215,"5d47b6ce","杨幂快来听"],[31.864,0,16777215,"c1bdb3e4","跪舔"],[55.683,0,16777215,"c1bdb3e4","现在也不错啊"],[164.948,0,16777215,"c1bdb3e4","唱功真好 "],[23.8,0,16777215,"c1bdb3e4","开口跪"],[83.85,0,16777215,"2da94dbc","岗岗"],[231.519,0,16777215,"adf68119","原来这几首歌这么好听"],[146.704,0,16777215,"2da94dbc","大咪咪能和她比唱"],[164.256,0,16777215,"43b8e2b2","那是汤镇宗"],[162.507,0,16777215,"43b8e2b2","那是段正淳，汤镇宗"],[238.24,0,16777215,"43b8e2b2","钟汉良甜蜜脸"],[317.121,0,16777215,"43b8e2b2","听岗岗唱两首歌，把刚下还没看的上原亚衣都删了"],[378.816,0,16777215,"43b8e2b2","跟王菲那英有什么关系，风格都不一样，你再看看王菲哪一年火的"],[73.099,0,16777215,"50d971d6","好喜欢她"],[207.499,0,16777215,"50d971d6","现在的她依旧那么甜啊！！"],[334.939,0,16777215,"50d971d6","开口跪！"],[365.419,0,16777215,"50d971d6","好甜好甜~"],[145.366,0,16777215,"a8f4f6f0","你很纯洁"],[347.845,0,16777215,"e7be12f1","她都快50了看着还像30多，真厉害"],[140.943,0,16777215,"6e2c6f33","好听啊！！"],[301.267,0,16777215,"6e2c6f33","她会煲汤啊！！！"],[81.479,0,16777215,"ceeadd93","杨幂哈哈哈"],[213.248,0,16777215,"ceeadd93","汤镇宗还是汤镇业是男主"],[24.825,0,0,"53a3b262","开口跪，胜过原唱万倍"],[206.822,0,0,"53a3b262","为什么突然看着像何洁"],[278.942,0,16777215,"1647e62","突然好羡慕赖昌星。。。"],[173.88,0,16777215,"f0ece025","好听"],[360.094,0,16777215,"a136ee9f","李涯？"],[308.88,0,16777215,"fe6085b5","说赖昌星的一定看了路边地摊的肮脏的书"],[109.98,0,16777215,"77355091","抱走峰峰"],[366.785,0,16777215,"9fc219ed","怎么就胖了呢"],[35.071,0,16777215,"8c3a1581","对口型也是人事先录的，你行你去啊？"],[123.904,0,16777215,"8c3a1581","啊啊啊啊啊忘了忘了，我们安徽电视台的国剧盛典都是现场真唱"],[175.701,0,16777215,"8c3a1581","国剧盛典都现场真唱的，别说她对口型啦，唱功在那里呢"],[213.077,0,16777215,"8c3a1581","啊啊啊啊刚刚一闪而过的慌张"],[208.213,0,16777215,"8c3a1581","乔任梁啊啊啊啊啊啊大哭"],[322.133,1,15138834,"8c3a1581","岗岗矫正过牙齿吗？"],[31.956,0,16777215,"47f6a970","杨幂听了都沉默"],[112.784,0,16777215,"47f6a970","周迅啊"],[193.18,0,16777215,"47eb6d45","一样的你，没改变"],[19.908,0,16777215,"68ee5c78","好听"],[89.895,0,16777215,"68ee5c78","喜欢杨钰莹岗岗"],[100.568,0,16777215,"68ee5c78","太美了"],[200.044,0,16777215,"68ee5c78","皮肤好好"],[141.427,1,16777215,"ddb25bec","莫名想起K娃的歌词。。。。。"],[284.221,0,16777215,"762485d2","前面赖昌星的，明明是赖文峰"],[311.903,0,16777215,"5a459c26","更成熟了"],[21.542,0,16777215,"27a292ae","还是好听啊"],[34.07,0,16777215,"27a292ae","现在更有知性美"],[146.94,0,16777215,"27a292ae","太棒了"],[198.67,0,16777215,"27a292ae","就算别人对口型，杨钰莹的实力，不需要对"],[253.15,0,16777215,"27a292ae","台风也好棒"],[342.216,0,16777215,"27a292ae","跪下听"],[25.046,0,0,"ec730332","冲动"],[106.379,0,16777215,"e86c4782","超级好听"],[140.373,0,16777215,"2c39528e","啊啊啊啊啊我的岗啊"],[209.066,0,16777215,"2c39528e","抓住小杰哥哥呀呀呀"],[75.621,0,16777215,"b6d9d070","声线迷人"],[402.928,0,16777215,"f8a11815","目瞪口呆！"],[17.801,0,16777215,"b7fba2ce","开口跪"],[352.536,0,16777215,"8bf942ea","和周璇差不多了"],[35.738,0,16777215,"52c54e58","配合打灰机很配哦"],[268.995,0,16777215,"e16302bb","上古大神"],[167.508,0,16777215,"4248f761","汤镇宗"],[184.362,0,16777215,"4248f761","外来妹"],[227.228,0,16777215,"4248f761","当然是汤镇宗男主"],[302.442,0,16777215,"2c39528e","95后表示岗岗一直是唯一的女神"],[8.726,0,16777215,"5173cb33","开口跪，为我岗打call"],[406.005,0,16777215,"5173cb33","太美了"],[406.804,0,16777215,"9805ed87","好享受啊"],[23.46,0,16777215,"3587b150"," 这版听起来超级高级"],[102.569,0,16777215,"8d2640b2","杨钰莹的歌很好听，人也美我喜欢"],[190.633,0,16777215,"4f22913e","天啊！！！唱得我心都酥了！！！"],[51.21,0,16777215,"2b5d499a","最好的版本没有之一"],[102.287,0,16777215,"4cfbe209","原来这首歌还能这么好听"],[27.039,0,16777215,"f5ffb76","造化弄人啊"],[372.939,0,16777215,"17330928","你能看见李涯了么？"],[21.33,0,16777215,"5e4285e","郑湫泓那弹幕过来的"],[289.195,0,16777215,"c9b75699","杨钰莹永远不翻车的"],[175.6,0,16777215,"9091f1a2","主演之一"],[179.697,0,16777215,"4c7f6fd7","汤镇宗是《外来妹》的男一号"],[13.379,0,16777215,"81df92e5","。"],[19.956,0,16777215,"4de11e12","女神！"],[141.581,0,16777215,"4de11e12","超爱女神"],[241.381,0,16777215,"4de11e12","最好听的，没有之一"],[71.857,0,16777215,"f388ec15","这才是唱歌，现在的，浮躁"],[267.211,0,16777215,"f642b11b","真的好厉害"],[224.284,0,16777215,"ba8f74e","眼睛真美..."],[147.284,0,16777215,"78630e0e","我不想说我是🐔的翻唱吗？"],[192.49,0,16777215,"ad1ebfda","这首歌是汤镇宗主要的电视剧的主题曲"],[336.529,0,16777215,"7fa66a6a","啊啊啊好甜好柔啊"],[196.12,0,16777215,"7ffa0a0","青春的记忆"],[241.741,0,16777215,"7ffa0a0","上歌手吧"],[332.999,0,16777215,"faa54a59","开口全身酥"],[378.333,0,16777215,"faa54a59","我不行了我不行了，听她唱歌得喝营养快线"],[380.744,0,16777215,"9701326c","下面的明星是要哭了?"],[124.213,0,16777215,"632ff605","岗岗失去的20年"],[70.932,0,16777215,"de70d4b4","她眼睛好亮"],[135.785,0,16777215,"de70d4b4","啊啊啊啊啊啊啊"],[98.831,0,16777215,"37fa743a","杨幂很尴尬"],[285.675,0,16777215,"37fa743a","细思极恐～"],[308.117,0,16777215,"6dfabfa0","00后惹你们了？"],[208.377,0,16777215,"dc4a9f58","杨钰莹保养的真是绝了，一点皱纹都没有"],[135.654,0,16777215,"304a544a","这首好好听"],[208.052,0,16777215,"b6e57c72","Kimi   "],[107.978,0,16777215,"7334ad33","好啊😊"],[323.837,0,16777215,"7334ad33","前方高能"],[100.279,0,16777215,"8589ce53","岗岗：老了，只能把你们吊起来打了。"],[144.705,0,16777215,"8589ce53","亲——切"],[77.098,0,16777215,"b86d45c6","個人覺得唱得比原唱好聽太多"],[147.579,0,16777215,"b86d45c6","實力唱功淋漓盡致"],[108.467,0,16777215,"ff1580c4","李沁哈哈哈"],[20.195,0,16777215,"93335a72","BGM爱的供养，再问自杀"],[283.38,0,16777215,"10c069c9","沁人心脾啊"],[302.379,0,16777215,"77bb9627","甜醉了"],[68.334,0,16777215,"2e4dda19","不得不说真的是吊打"],[82.128,0,16777215,"7de9f6d1","杨幂的都修出电音来了"],[304.234,0,16777215,"4abb6aa3","无论是否假唱 杨钰莹的实力不至于怀疑"],[51.539,0,16777215,"bc932230","真正的歌手"],[35.108,0,16777215,"faa54a59","造化弄人啊"],[200.581,0,16777215,"faa54a59","太迷人了……简直是声音外型气质的完美结合"],[340.736,0,16777215,"faa54a59","唱出花来的那位请留步，你说出我心声了，谢谢！"],[362.416,0,16777215,"faa54a59","这个舌头舔得，啧啧啧，换我哈喇子早流下来了"],[338.926,0,16777215,"faa54a59","开口这句真的心都酥了"],[168.209,0,16777215,"b801a2b2","伯异考?"],[15.521,0,16777215,"7923315d","开口跪"],[40.141,0,16777215,"7923315d","这首歌这么好听吗？？"],[101.064,0,16777215,"4f6d8dd1","这真是温柔乡啊"],[81.772,0,16777215,"fb72e38","眼睛好漂亮"],[160.348,0,16777215,"8017676f","有人能感受到这是一位阿姨吗？"],[204.795,0,16777215,"8017676f","我说，还用对口型吗？记得天津电视台的节目观众现场点邓丽君的歌，杨钰莹直接就唱了一遍。"],[58.739,0,16777215,"d320f48","真羡慕这种还是那么年轻漂亮的人"],[156.852,0,16777215,"4c15dfb1","当年男主啊～汤镇宗"],[61.072,0,16777215,"fbee7be8","这个有点难度，难为我大幂幂了啊"],[198.304,0,16777215,"fbee7be8","我靠，大家都对汤镇宗有印象哈，还有伯邑考"],[223.094,0,16777215,"fbee7be8","汤镇业"],[84.842,0,16777215,"7a40e02f","觉得声音很高昂 发声位置是不是挺讲究"],[192.311,0,16777215,"7a40e02f","女人活到这境界才叫值"],[145.37,0,16777215,"b5954462","真的好听"],[160.876,0,16777215,"b5954462","小时候超级爱她，甜甜的长相和歌声"],[9.412,0,16777215,"3342ebf","好好听"],[206.515,0,16777215,"f8f1b97d","杨钰莹唱痒会怎么样？"],[18.817,0,16777215,"f01a8554","杨幂，你看看人家"],[181.081,0,16777215,"a0715c40","胰岛素，受不了了"],[73.938,0,16777215,"965e843a","不错"],[100.744,0,16777215,"91399a56","杨幂版本的调音师辛苦了"],[10.876,0,16777215,"b0256015","太好听了"],[51.665,0,16777215,"b0256015","三十岁仍然喜欢杨钰莹的歌 太甜了"],[214.097,0,16777215,"b0256015","陈伟霆"],[279.603,0,16777215,"fa7bf3c4","可你忘了这样的女孩子大概自己就能活得像诗一样了吧"],[275.748,0,16777215,"9adf2046","这个年纪了嗓音好这么清澈气息控制这么好真的太厉害了"],[58.072,0,16777215,"2736860","竟然看到我们诗诗"],[404.269,0,16777215,"7b0415a5","美得想哭"],[14.975,0,16777215,"ec31a203","哇塞"],[65.052,0,16777215,"5438c7fc","好听"],[12.202,0,16777215,"3c7120a6","气息不够不是年龄问题吧，很多老歌唱家怎么说？"],[7.062,0,16777215,"b49255fe","前面的还没听呢就知道气不够了？？"],[159.379,0,16777215,"d864208","听着这歌长大的。。。"],[259.655,0,16777215,"d864208","唱功给跪。。。"],[361.288,0,16777215,"d864208","听得我打了个寒颤，然后感觉素然无味。。。"],[165.806,0,16777215,"64a6d1d8","远古大神"],[193.46,0,16777215,"8e80a82f","杨钰莹也四十多了啊"],[287.063,0,16777215,"8e80a82f","你很难相信她都超过四十五岁了"],[25.299,0,16777215,"fa7bf3c4","哇头发好好看(●—●)"],[25.806,0,16777215,"ec730332","女神啊！"],[274.861,0,16777215,"ec730332","痒得不行"],[169.4,0,16777215,"ec730332","多了更多的成熟美"],[337.139,0,16777215,"6c03fa47","周璇的歌，我的妈呀"],[389.859,0,16777215,"6c03fa47","当时金童玉女火透天际"],[31.541,0,16777215,"9195dd1f","太美了"],[39.468,0,16777215,"c7da2703","好听，比杨幂强到天上去了"],[238.639,0,16777215,"c7da2703","杨钰莹可不能唱痒，不然听众都痒死了……"],[329.955,0,16777215,"c7da2703","杨钰莹那个时代，还没有假唱这一说呢"],[384.389,0,16777215,"c7da2703","这声音甜的，酥了"],[331.151,0,16777215,"65bd8e20","第一次听到是血战上海滩通关后"],[30.014,0,16777215,"b0256015","只听杨钰莹和费玉清唱的爱的供养 "],[32.342,0,16777215,"965e843a","女神"],[194.954,0,16777215,"8ab1f28e","醉了。。。"],[102.374,0,16777215,"8ab1f28e","超级好听啊"],[281.34,0,16777215,"af75f9c0","保护起来"],[90.132,0,16777215,"40dcb23a","比台下各路小花都好看啊！！！！！！"],[186.483,0,16777215,"40dcb23a","汤镇宗是这电视剧男一号吧"],[29.311,0,16777215,"38678e9f","还是比原唱好很多"],[385.732,0,16777215,"c5c47e1a","当年如果跟了赖家出事，估计后来也没有那英这些人什么事了"],[86.961,0,16777215,"8c5f02b","杨幂:55555555"],[97.831,0,16777215,"5ae1f87","听的第三个版本 也是 最好听的一版"],[126.471,0,16777215,"c71e3f80","感觉比杨幂好听太多。。"],[35.754,0,16777215,"bff3cc6f","比原唱好听"],[74.7,0,16777215,"b65f8da2","啊啊啊AA啊啊啊啊啊 好听"],[79.864,0,16777215,"b65f8da2","真唱"],[215.145,0,16777215,"b65f8da2","被岁月温柔以待的女人"],[203.224,0,16777215,"b65f8da2","风采依旧啊"],[324.152,0,16777215,"b65f8da2","前面说捧的 你是瞎还是聋"],[277.601,0,16777215,"b65f8da2","杨钰莹很难被模仿 她的转音太厉害了"],[375.104,0,16777215,"b65f8da2","那叫富态"],[183.945,0,16777215,"b65f8da2","很漂亮"],[112.817,0,16777215,"74efa7ca","气息不稳气息不够，毕竟年纪上去了"],[187.056,0,16777215,"74efa7ca","怀念的嗓音，可以不是当年的感觉"],[250.016,0,16777215,"74efa7ca","真的很甜啊"],[359.509,0,16777215,"a63a16d8","哇都是欣赏的眼神啊"],[30.023,0,15138834,"1aece0af","这就是女神开口跪"],[97.352,0,15138834,"1aece0af","就是这个长字，台下各位没有一个能唱的出"],[170.671,0,15138834,"1aece0af","外来妹男主"],[347.712,0,15138834,"1aece0af","气息，不是假唱"],[66.474,0,16777215,"d35a5604","好听哭了"],[160.597,0,16777215,"d35a5604","怎么能这么好听呢"],[269.822,0,16777215,"c6c62a60","好喜欢"],[48.758,0,15138834,"1aece0af","这个转音，无人能敌"],[336.611,0,15138834,"1aece0af","全身酥酥"],[380.211,0,15138834,"1aece0af","竟然能听流眼泪"],[267.697,0,16777215,"8a0a8018","让赖氏父子糟蹋了"],[157.039,0,16777215,"d54b2ef9","现在的都是假唱，可惜你们都喜欢资本都喜欢假唱"],[216.133,0,16777215,"1aece0af","前方高能了"],[136.145,0,16777215,"2118372d","杨钰莹真的好漂亮"],[108.831,0,16777215,"2118372d","人美歌甜"],[358.412,0,16777215,"2118372d","一开口花都开了"],[28.166,0,16777215,"739a158d","@杨幂 进来挨打"],[88.034,0,16777215,"3c5386dd","这一听就是用丹田唱歌啊，幂幂感觉声音在喉咙里"],[212.633,0,16777215,"3c5386dd","唱得真的蛮好的，"],[97.649,0,16777215,"a4d52734","好好听啊"],[137.467,0,16777215,"fa3b0c55","差点泪目....00后表示好爱她。"],[51.44,0,16777215,"3ef74a79","这明显真唱，假唱是播放处理过的，会好听很多"],[50.884,0,16777215,"c23f1d3f","以前的歌手真的是歌手"],[77.141,0,16777215,"dc8d9ad4","比一众小花都好看"],[73.956,0,16777215,"4e597229","周慧敏 孟庭苇 杨钰莹  这三个应该搞个组合"],[173.653,0,16777215,"9bdcfbb4","为岗岗打 call"],[302.221,0,16777215,"fa3b0c55","03嘻嘻 特别 喜欢她"],[275.142,0,16777215,"ef334f5c","其实是当时的社会糟蹋了她吧 男人们都觉得这样的女人肯定要做二奶 女人们都觉得这样的女人勾引了她们的男人"],[277.878,0,16777215,"ef334f5c","但是被耽误了近二十年青春岁月的杨钰莹如今重上舞台，依旧用她不老的容颜讲述着永存的青春"],[142.517,0,16777215,"7dfdc8e8"," 太喜欢这首歌了只有她唱才有那种效果"],[114.661,0,16777215,"d7a4cbc2","我说秒杀原唱各位没意见吧？"],[14.608,0,16777215,"f31ee42","好听"],[197.837,0,16777215,"4fc02242","80后知道这剧这歌当年有多火"],[164.89,0,16777215,"4fc02242","男主"],[243.182,0,16777215,"4fc02242","80后的大姐姐，这三部剧都看过啊太熟悉了"],[275.088,0,16777215,"54a42c92","真女神！"],[211.622,0,16777215,"cdf02c59","这才是歌手啊，现在的歌手都唱的什么玩意儿"],[211.756,0,16777215,"fd0c7f11","90年代唱这首歌的时候那颜值真的是漂亮啊"],[179.645,0,16777215,"9526db58","话说，不管是歌声还是容貌，她都能秒杀现在很多流量小花"],[17.012,0,16777215,"3151c91c","演出好棒ヾ ^_^♪"],[24.813,0,16777215,"3151c91c","看看台下听众们的表情就知道，这段表演是多么精彩！杨钰莹心中始终坚持一份美好，特别是对音乐的爱(⑉°з°)-♡"],[147.133,0,16777215,"3151c91c","耳朵怀孕了"],[155.813,0,16777215,"3151c91c","请关注台下听众们的表情～"],[246.611,0,16777215,"3151c91c","台下的人都醉了～～～"],[333.211,0,16777215,"3151c91c","后面的这首～月圆花好～简直是精彩到不行～"],[106.516,0,16777215,"31ec1310","轻轻地翻唱"],[111.719,0,16777215,"63f98db6","吊打原唱"],[56.102,2,14811775,"3263405c","吼吼听"],[167.68,0,16777215,"4fa282e7","甜甜小妹"],[234.523,0,16777215,"126043e","零零后迷上她了"],[159.05,0,16777215,"8017676f","萨日娜！"],[78.154,0,16777215,"8017676f","周慧敏 孟庭苇 杨钰莹搞组合？不被杨钰莹压倒？"],[23.093,0,16777215,"d189452e","真的好棒"],[142.024,0,16777215,"54a42c92","好美啊！"],[137.531,0,16777215,"2a1948ef","童年的歌！回忆啊"],[273.186,0,16777215,"2a1948ef","好喜欢她啊呜呜呜呜"],[334.2,0,16777215,"4e597229","84年出生。杨钰莹儿时女神"],[160.239,0,16777215,"81bf9ba6","回忆杀"],[255.971,0,16777215,"81bf9ba6","人美歌甜"],[383.246,0,16777215,"81bf9ba6","毛宁哪去了"],[75.419,0,16777215,"61df2d2a","我特别爱醉好年龄稍微大一点的女人。感觉有因为特过瘾。"],[97.419,0,16777215,"61df2d2a","年龄大一点的女人，美丽的女人，刺激过瘾。"],[10.878,0,16777215,"61df2d2a","外来妹好听。"],[142.659,0,16777215,"61df2d2a","这歌好听。"],[33.318,0,16777215,"61df2d2a","杨幂幂公主，你快来听有人为你演绎。主题歌啦。"],[66.717,0,16777215,"61df2d2a","真不知道为什么她这么大岁数我还爱他。难道我是疯子？不是因为我懂音乐。爱的真谛。我也怎么不知道看到女人就喜欢。"],[109.238,0,16777215,"61df2d2a","她绝不是花瓶。"],[94.437,0,16777215,"61df2d2a","杨钰莹有真才实学的唱功和实力。所以他会第二次辉煌成功。而且他虽然是40岁了，但是呢好多男人还是想他。"],[119.958,0,16777215,"61df2d2a","他的作品当中透露出了健康。美丽公平正义，善良，纯真。"],[158.158,0,16777215,"61df2d2a","刚刚绝不是。媚俗低俗，俗气的一类。她是纯洁的女生。"],[168.998,0,16777215,"61df2d2a","她的苦。他的爱。只有他自己知道。那就是毛宁"],[191.238,0,16777215,"61df2d2a","外来妹是一首苗说普通打工的外来。打工女的坎坷的一生。这是健康的作品。"],[332.251,0,16777215,"61df2d2a","她的作品。充满着底层人民生活的悲欢离合。"],[6.558,0,16777215,"61df2d2a","他的作品充满着。底层人民的生活的悲欢离合和人性的普通的爱，纯洁的爱，可贵的爱真善美的伟大的有车不朽的大爱。"],[273.718,0,16777215,"61df2d2a","艺人也是人。，大家原谅他吧。"],[64.997,0,16777215,"61df2d2a","大幂幂，你快来看看有人在深情演绎你的歌啦！"],[23.958,0,16777215,"61df2d2a","大幂幂乖女儿。啊，你快来看看有人在深情演绎你的歌啦。"],[89.758,0,16777215,"61df2d2a","我喜欢年龄大的女人。"],[103.112,0,16777215,"61df2d2a","我喜欢年龄大的女人，感觉她们。这些女人。特懂事。和明白事理。和成熟。有美丽的女人味。"],[193.278,0,16777215,"61df2d2a","有努力就会成功。"],[209.278,0,16777215,"61df2d2a","80至90年代打工妹的人生。悲惨生活。心声。"],[21.078,0,16777215,"61df2d2a","气不够是年龄的问题。不能怪他。"],[96.917,0,16777215,"61df2d2a","大家有没有从他的歌声中清楚他的谦虚和。和谐。和尊重，谦卑。这就是一首音乐成功的关键。也是小妹一生悲欢离合的写照。"],[33.238,0,16777215,"61df2d2a","他在拼搏。忘我的拼搏。把最美的无私的歌声奉献给人间。希望人间多一些。快乐。"],[86.078,0,16777215,"61df2d2a","我喜欢年龄大一点的女人，有女人味。"],[348.381,0,16777215,"bc4dc895"," 这才叫音乐艺术"],[272.671,0,16777215,"79d52ae0","扇子－裙里好凉快！"],[93.319,0,16777215,"1e2bc659","比大咪咪强万倍"],[38.771,0,16777215,"797b0565","杨幂都不敢来"],[302.7,0,16777215,"ff129910","看着哭了"],[286.754,0,16777215,"ff129910","女神"],[397.364,0,16777215,"5dec15f1","另一个朋友，是不是和我一样在洗脑循环啊"],[381.423,0,16777215,"85e5a0b6","需要胰岛素"],[363.123,1,16646914,"675d1b90","底下纵星：骨头酥了 扛不住！"],[21.026,0,16777215,"cbc362e0","哇这个爱的供养真的 太惊艳了"],[398.219,0,16777215,"c9535e9d","啊，这手指，我死了"],[362.227,1,16646914,"675d1b90","营养快线来一箱"],[282.654,0,16777215,"ecd367a2","她和毛宁真是唱歌没换气声的那种强"],[406.847,0,16777215,"ecd367a2","演员脸，比很多演员都漂亮"],[370.739,0,16777215,"ecd367a2","有点延迟，她这种水平的根本用不着假唱了"],[387.96,0,16777215,"675d1b90","666666666666666"],[27.929,0,16777215,"d55fbc02","柔情似水"],[344.699,0,16777215,"52a4173f","呵呵 上原亚衣 的 那个 等等"],[41.799,0,16777215,"5200e8bd","好美哦"],[193.431,0,16777215,"5200e8bd","又甜又很轻松写意"],[8.829,0,16777215,"829781a3","爱的自杀"],[34.205,0,16777215,"829781a3","杨幂唱的好"],[82.313,0,16777215,"829781a3","杨幂进来挨打"],[6.214,0,16777215,"21d31615","现在终于知道中文歌听不下去了 原来小时候听过杨女神的歌 耳朵就已经无法再听进其他中文歌了"],[75.921,0,16777215,"49518c17","眼睛亮是美瞳"],[20.773,0,16777215,"5173cb33","岗岗真棒"],[347.843,0,16777215,"5173cb33","无与伦比的美丽"],[102.762,0,16777215,"a27e78a","杨幂和她比？她是初代歌姬好么"],[318.677,0,16777215,"a27e78a","红楼的事并不是小道消息是事实好么"],[378.217,0,16777215,"a27e78a","杨钰莹可能是台下许多明星的童年偶像"],[48.358,0,16777215,"299797bd","不老女神"],[248.648,0,16777215,"2189e209","声音没年轻时甜了"],[6.544,0,16777215,"35d0bb5c","第一次觉得爱的保养这么好听"],[33.302,0,16777215,"35d0bb5c","原来这歌这么好听"],[164.354,0,16777215,"35d0bb5c","伯邑考？"],[152.072,0,16777215,"8300f69e","这是时代曲了"],[84.341,0,16777215,"b3f311eb","前面组组合的我同意哈哈"],[147.964,0,16777215,"b3f311eb","哎岁月"],[26.517,0,16777215,"4a7865b3","神颜值"],[239.649,0,16777215,"4a7865b3","高能"],[353.251,0,16777215,"4a7865b3","有提词器吗？"],[277.144,0,16777215,"4298e10","说她30岁应该都会信吧"],[9.696,0,16646914,"b3f311eb","@杨幂 进来挨打"],[185.685,0,16777215,"b3f311eb","陈赫这什么鬼表情"],[362.312,0,16777215,"94bb81f8","适合配点小酒 赏着月 坐在庭院里，醉人"],[349.374,0,16777215,"f94a98df","经她一唱真的是月圆花好啊"],[341.878,0,16777215,"e891838c","开声了"],[60.53,0,16777215,"8fbba5a0","杨幂现场版简直尴尬"],[293.902,0,16777215,"8fbba5a0","好甜呀"],[340.165,0,16777215,"3c5386dd","宝刀未老"],[121.036,0,16777215,"c506c8c4","杨幂唱歌咬字太死了"],[79.076,0,16777215,"c4d1a531","这才叫享受"],[361.856,0,16777215,"ee855794","这女的是谁"],[188.894,0,16777215,"cb6e394a","这句歌词太符合杨钰莹这20年曲折人生的写照了，她和这首歌真是天作之合。"],[40.206,0,16777215,"a128423f","这歌还是得看谁唱啊"],[104.285,0,16777215,"daa97a92","这才叫真正的唱歌"],[73.772,1,9487136,"478696a3","这个是谁？↓"],[186.585,0,16777215,"b86d45c6","杨钰莹唱功内地乐坛首屈一指"],[114.176,0,16777215,"15964085","好听"]]}

        return JsonResponse(mydm,json_dumps_params={'ensure_ascii':False})