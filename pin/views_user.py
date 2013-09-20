# -*- coding: utf-8 -*-
from time import time
import json
import datetime
import urllib
from shutil import copyfile

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from pin.crawler import get_images
from pin.forms import PinForm, PinUpdateForm
from pin.models import Post, Stream, Follow, Likes, Notif, Notif_actors,\
    Report, Comments, Comments_score, Category

import pin_image
from pin.tools import get_request_timestamp, create_filename, get_user_ip

from user_profile.models import Profile

MEDIA_ROOT = settings.MEDIA_ROOT


@login_required
def following(request):
    timestamp = get_request_timestamp(request)

    if timestamp == 0:
        stream = Stream.objects.filter(user=request.user)\
            .order_by('-date')[:20]
    else:
        stream = Stream.objects.filter(user=request.user)\
            .extra(where=['date<%s'], params=[timestamp])\
            .order_by('-date')[:20]

    idis = []
    for p in stream:
        idis.append(int(p.post_id))

    latest_items = Post.objects.filter(id__in=idis, status=1)\
        .all().order_by('-id')

    sorted_objects = latest_items

    if request.is_ajax():
        if latest_items.exists():
            return render(request,
                          'pin/_items.html',
                          {'latest_items': sorted_objects})
        else:
            return HttpResponse(0)
    else:
        return render(request,
                      'pin/home.html',
                      {'latest_items': sorted_objects})


@login_required
def follow(request, following, action):
    if int(following) == request.user.id:
        return HttpResponseRedirect(reverse('pin-home'))

    try:
        following = User.objects.get(pk=int(following))

        follow, created = Follow.objects.get_or_create(follower=request.user,
                                                       following=following)

        if int(action) == 0:
            follow.delete()
            Stream.objects.filter(following=following, user=request.user)\
                .all().delete()
        else:
            posts = Post.objects.filter(user=following, status=1)[:100]
            with transaction.commit_on_success():
                for post in posts:
                    stream = Stream(post=post,
                                    user=request.user,
                                    date=post.timestamp,
                                    following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('pin-user', args=[following.id]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('pin-user', args=[following.id]))


@login_required
def like(request, item_id):
    try:
        post = Post.objects.get(pk=item_id, status=1)
        current_like = post.cnt_likes()

        try:
            liked = Likes.objects.get(user=request.user, post=post)
            created = False
        except Likes.DoesNotExist:
            liked = Likes.objects.create(user=request.user, post=post)
            created = True

        if created:
            current_like = current_like + 1
            user_act = 1

            liked.ip = request.META.get("REMOTE_ADDR", '127.0.0.1')
            liked.save()
        elif liked:
            current_like = current_like - 1
            Likes.objects.get(user=request.user, post=post).delete()
            user_act = -1

        try:
            profile = Profile.objects.get(user=post.user)
            profile.save()
        except Profile.DoesNotExist:
            pass

        if request.is_ajax():
            data = [{'likes': current_like, 'user_act': user_act}]
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponseRedirect(reverse('pin-item', args=[post.id]))

    except Post.DoesNotExist:
        return HttpResponseRedirect('/')


@login_required
def notif_user(request):
    timestamp = get_request_timestamp(request)
    if timestamp:
        date = datetime.datetime.fromtimestamp(timestamp)
        notif = Notif.objects.filter(user_id=request.user.id, date__lt=date)\
            .order_by('-date')[:20]
    else:
        notif = Notif.objects.filter(user_id=request.user.id)\
            .order_by('-date')[:20]

    for n in notif:
        n.actors = Notif_actors.objects.filter(notif=n).order_by('-id')[:20]

    if request.is_ajax():
        return render(request, 'pin/_notif.html', {'notif': notif})
    else:
        return render(request, 'pin/notif_user.html', {'notif': notif})


@login_required
def report(request, pin_id):
    try:
        post = Post.objects.get(id=pin_id)
    except Post.DoesNotExist:
        return HttpResponseRedirect('/')

    try:
        Report.objects.get(user=request.user, post=post)
        created = False
    except Report.DoesNotExist:
        Report.objects.create(user=request.user, post=post)
        created = True

    if created:
        if post.report == 9:
            post.status = 0
        post.report = post.report + 1
        post.save()
        status = True
        msg = 'گزارش شما ثبت شد.'
    else:
        status = False
        msg = 'شما قبلا این مطلب را گزارش داده اید.'

    if request.is_ajax():
        data = [{'status': status, 'msg': msg}]
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponseRedirect(reverse('pin-item', args=[post.id]))


@login_required
def comment_score(request, comment_id, score):
    score = int(score)
    scores = [1, 0]
    if score not in scores:
        return HttpResponse('error in scores')

    if score == 0:
        score = -1

    try:
        cm = Comments.objects.get(pk=comment_id)
        user = request.user
        cs, cd = Comments_score.objects.get_or_create(user=user, comment=cm)
        if score != cs.score:
            cs.score = score
            cs.save()

        sum_score = Comments_score.objects.filter(comment=cm)\
            .aggregate(Sum('score'))

        cm.score = sum_score['score__sum']
        cm.save()

        return HttpResponse(sum_score['score__sum'])

    except Comments.DoesNotExist:
        return HttpResponseRedirect('/')


@login_required
def delete(request, item_id):
    try:
        post = Post.objects.get(pk=item_id)
        if post.user == request.user or request.user.is_superuser:
            post.delete()
            return HttpResponse('1')

    except Post.DoesNotExist:
        return HttpResponse('0')

    return HttpResponse('0')


@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_active, login_url='/pin/you_are_deactive/')
def send_comment(request):
    if request.method == 'POST':
        text = request.POST.get('text', None)
        post = request.POST.get('post', None)
        if text and post:
            post = get_object_or_404(Post, pk=post)
            Comments.objects.create(object_pk=post,
                                    comment=text,
                                    user=request.user,
                                    ip_address=get_user_ip(request))

            return HttpResponseRedirect(reverse('pin-item', args=[post.id]))

    return HttpResponse('error')


def you_are_deactive(request):
    return render(request, 'pin/you_are_deactive.html')


@login_required
def sendurl(request):
    if request.method == "POST":
        post_values = request.POST.copy()
        tags = post_values['tags']
        post_values['tags'] = tags[tags.find("[")+1:tags.find("]")]
        form = PinForm(post_values)
        if form.is_valid():
            model = form.save(commit=False)

            image_url = model.image
            filename = image_url.split('/')[-1]
            filename = create_filename(filename)
            image_on = "%s/pin/images/o/%s" % (MEDIA_ROOT, filename)

            urllib.urlretrieve(image_url, image_on)

            model.image = "pin/images/o/%s" % (filename)
            model.timestamp = time()
            model.user = request.user
            model.save()

            form.save_m2m()

            if model.status == 1:
                msg = 'مطلب شما با موفقیت ارسال شد. <a href="%s">مشاهده</a>' %\
                    reverse('pin-item', args=[model.id])
                messages.add_message(request, messages.SUCCESS, msg)
            elif model.status == 0:
                msg = 'مطلب شما با موفقیت ارسال شد و بعد از تایید در سایت نمایش داده می شود '
                messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect('/pin/')
    else:
        form = PinForm()

    return render(request, 'pin/sendurl.html', {'form': form})


@login_required
@csrf_exempt
def a_sendurl(request):
    if request.method == "POST":
        url = request.POST['url']

        if url == '':
            return HttpResponse(0)

        images = get_images(url)
        if images == 0:
            return HttpResponse(0)

        return HttpResponse(json.dumps(images))
    else:
        return HttpResponse(0)


@login_required
def send(request):
    if request.method == "POST":
        post_values = request.POST.copy()
        tags = post_values['tags']
        post_values['tags'] = tags[tags.find("[") + 1:tags.find("]")]
        form = PinForm(post_values)
        if form.is_valid():
            model = form.save(commit=False)
            filename = model.image
            image_o = "%s/pin/temp/o/%s" % (MEDIA_ROOT, filename)
            image_on = "%s/pin/images/o/%s" % (MEDIA_ROOT, filename)

            copyfile(image_o, image_on)

            model.image = "pin/images/o/%s" % (filename)
            model.timestamp = time()
            model.user = request.user
            model.save()

            form.save_m2m()

            if model.status == 1:
                msg = 'مطلب شما با موفقیت ارسال شد. <a href="%s">مشاهده</a>' %\
                    reverse('pin-item', args=[model.id])
                messages.add_message(request, messages.SUCCESS, msg)
            elif model.status == 0:
                msg = 'مطلب شما با موفقیت ارسال شد و بعد از تایید در سایت نمایش داده می شود '
                messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect('/pin/')
    else:
        form = PinForm()

    category = Category.objects.all()

    if request.is_ajax():
        return render(request, 'pin/_send.html', {'form': form, 'category': category})
    else:
        return render(request, 'pin/send.html', {'form': form, 'category': category})


@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(pk=int(post_id))
        if not request.user.is_superuser:
            if post.user.id != request.user.id:
                return HttpResponseRedirect('/pin/')

        if request.method == "POST":
            post_values = request.POST.copy()
            tags = post_values['tags']
            post_values['tags'] = tags[tags.find("[") + 1:tags.find("]")]
            form = PinUpdateForm(post_values, instance=post)
            if form.is_valid():
                model = form.save(commit=False)
                model.save()
                form.save_m2m()

                return HttpResponse('با موفقیت به روزرسانی شد.')
        else:
            form = PinUpdateForm(instance=post)

        if request.is_ajax():
            return render(request, 'pin/_edit.html', {'form': form, 'post': post})
        else:
            return render(request, 'pin/edit.html', {'form': form, 'post': post})
    except Post.DoesNotExist:
        return HttpResponseRedirect('/pin/')


def save_upload(uploaded, filename, raw_data):
    ''' raw_data: if True, upfile is a HttpRequest object with raw post data
        as the file, rather than a Django UploadedFile from request.FILES '''
    try:
        from io import FileIO, BufferedWriter
        with BufferedWriter(FileIO("%s/pin/temp/o/%s" % (MEDIA_ROOT, filename), "wb")) as dest:

            if raw_data:
                foo = uploaded.read(1024)
                while foo:
                    dest.write(foo)
                    foo = uploaded.read(1024)

            else:
                for c in uploaded.chunks():
                    dest.write(c)
            return True
    except IOError:
        # could not open the file most likely
        return False


@csrf_exempt
def upload(request):
    if request.method == "POST":
        if request.is_ajax():
            upload = request
            is_raw = True
            try:
                filename = request.GET['qqfile']
            except KeyError:
                return HttpResponseBadRequest("AJAX request not valid")
        else:
            is_raw = False
            if len(request.FILES) == 1:
                upload = request.FILES.values()[0]
            else:
                raise Http404("Bad Upload")
            filename = upload.name

        filename = create_filename(filename)
        success = save_upload(upload, filename, is_raw)
        if success:
            image_o = "%s/pin/temp/o/%s" % (MEDIA_ROOT, filename)
            image_t = "%s/pin/temp/t/%s" % (MEDIA_ROOT, filename)

            pin_image.resize(image_o, image_t, 99)

        ret_json = {'success': success, 'file': filename}
        return HttpResponse(json.dumps(ret_json))


@login_required
def show_notify(request):
    Notif.objects.filter(user_id=request.user.id, seen=False).update(seen=True)
    notif = Notif.objects.all().filter(user_id=request.user.id).order_by('-date')[:20]
    for n in notif:
        n.actors = Notif_actors.objects.filter(notif=n)
    return render(request, 'pin/notify.html', {'notif': notif})
