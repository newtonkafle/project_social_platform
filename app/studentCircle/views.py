from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from core.models import Room, Topic, User, Messages
from core.forms import RoomForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        user = None
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is not correct')

    context = {'page': page}
    return render(request, 'login_register.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            send_verification_email(request, user, 'AA')
            messages.success(
                request, 'Verification link has been sent to email')
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registrations')
    context = {'form': form}

    return render(request, 'login_register.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        messages.error(request, 'Activation failed, Activation link invalid!')
    else:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account activation successfull. ')
        else:
            messages.error(
                request, 'Activation failed, Activation link expired!'
            )
    finally:
        return redirect('login')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:4]
    room_count = rooms.count()

    room_activity = Messages.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_activity': room_activity}
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.messages_set.all().order_by('-created_at')
    participants = room.participants.all()

    if request.method == "POST":
        message = Messages.objects.create(
            user=request.user,
            room=room,
            message=request.POST['room_message'],
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'room.html', context)


def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_activity = user.messages_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'rooms': rooms,
               'room_activity': room_activity,
               'topics': topics}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),

        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Unauthorized')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'room_form.html', context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Unauthorized')

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': room})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Messages.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Unauthorized')

    if request.method == "POST":
        message.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):

    form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            return redirect('user-profile', id=user.id)
    context = {'form': form, 'p_form': p_form}
    return render(request, 'edit-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'topics.html', context)


def activityPage(request):
    room_messages = Messages.objects.all()
    context = {'room_activity': room_messages}
    return render(request, 'activity.html', context)


# handling forgor password
def forgotPassword(request):
    """ view for handling the forgot password"""
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            send_verification_email(request,
                                    user,
                                    'RP')

            messages.success(
                request, 'Password reset link sent to your email!')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgot-password')

    return render(request, 'forgot_pass.html')


def resetPasswordValidate(request, uidb64, token):
    """ view to validate the request to reset the password"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(
            request, 'Link Error, Password reset link has been modified!')
        return redirect('forgot-password')
    else:
        if default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect('reset-password')
        else:
            messages.error(
                request, 'Password reset failed, The link has been expired!')
            return redirect('forgot-password')


def resetPassword(request):
    """ view to reset the password"""
    # bugs check and error handling required
    if request.method == 'POST':
        password = request.POST['password']
        conf_password = request.POST['conf_password']

        if password == conf_password:
            try:
                pk = request.session.get('uid')
                user = User.objects.get(pk=pk)

            except User.DoesNotExist:
                return redirect('login')
            else:
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request, 'Password reset successful')
                del request.session['uid']
                return redirect('login')
        else:
            messages.error("Password doesn't match")
            return redirect('reset-password')

    return render(request, 'reset_password.html')
