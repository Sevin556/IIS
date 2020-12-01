from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .backend import AuthBackend
import django.contrib.auth.hashers as hasher
from django.contrib.auth import authenticate, login, logout
from .models import t_festival, t_stage, t_listok, t_interpret, r_zucastni_sa, r_vystupuje_na, Additional, r_rezervacia_na, t_rezervacia
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
import datetime, operator
import dateutil.parser

from .forms import NewFestivalForm, NewStageForm, NewInterpretForm, NewTicketForm
# Create your views here.


def home(request):
    if request.method == 'POST':
        festival_name = request.POST['fest_name']
        interpret_name = request.POST['interpret_name']
        start_string = request.POST['start_date']
        end_string = request.POST['end_date']
        festivals = t_festival.objects.all().order_by('zaciatok')

        if not start_string =="":
            start_date = dateutil.parser.parse(start_string)
        else:
            start_date = None

        if not end_string =="":
            end_date = dateutil.parser.parse(end_string)

        else:
            end_date = None
        if not festival_name == "":
            print("filter name")
            festivals = festivals.filter(nazov__icontains=festival_name)
        if not interpret_name == "":
            print("filter inter")
            interprets = t_interpret.objects.filter(nazov__icontains=interpret_name)
            zucastneni = r_zucastni_sa.objects.all()
            first = True
            query = Q(id=-1)
            for item in zucastneni:
                for interpret in interprets:
                    if item.id_interpret.id == interpret.id:
                        if first:
                            query = Q(id=item.id_festival.id)
                            first = False
                        else:
                            query.add(Q(id=item.id_festival.id), Q.OR)
            festivals = festivals.filter(query)
        if not start_date == None:
            print("filter start")
            festivals = festivals.filter(koniec__gte=start_date)
        if end_date != None:
            print("filter end")
            festivals = festivals.filter(koniec__lte=end_date)

        Content = {'festivals': festivals}
        render(request, 'festivals/home.html', Content)

    else:
        Content = {
            'festivals': t_festival.objects.filter(zaciatok__gte=datetime.date.today())
        }
    return render(request, 'festivals/home.html', Content)


def login_view(request):
    if request.method == 'POST':
        u_email = request.POST['email']
        u_password = request.POST['password']

        try:
            user = authenticate(request, username=u_email, password=u_password)
        except AuthBackend.BadEmail:
            messages.warning(request, f'Invalid email!')
            return render(request, 'authentication/login.html')
        except AuthBackend.BadPassword:
            messages.warning(request, f'Incorrect password!')
            return render(request, 'authentication/login.html')

        # success
        if(user):
            login(request, user)
            messages.success(request, f"You have been successfully logged in!")
            return redirect('festivals-home')
        else:
            messages.warning(request, f'ILogin failed!')
            return render(request, 'authentication/login.html')
    else:
        # GET
        return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    try:
        del request.session['session_uid']
    except KeyError:
        pass

    messages.success(request, f"You have been successfully logged out!")

    return redirect('festivals-home')


def register_view(request):
    if request.method == 'POST':
        u_name = request.POST['name']
        u_surname = request.POST['surname']
        u_email = request.POST['email']
        u_rawpassword = request.POST['password']

        # try finding user in user database
        try:
            User.objects.get(username=u_email)

            # user with same email found
            messages.warning(request, f"Email already in use!")
            return render(request, 'authentication/register.html')
        except User.DoesNotExist:
            # user not found, continue
            pass

        # add user to database
        new_user = User.objects.create_user(username=u_email, first_name=u_name, last_name=u_surname, email=u_email, password=u_rawpassword)
        new_user.save()

        additional_info = Additional(user=new_user)
        additional_info.display_name = u_name[0] + ". " + u_surname
        additional_info.save()

        messages.success(request, f"Account successfully created!")

        return redirect('festivals-login')
    else:
        return render(request, 'authentication/register.html')


def newFestival(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewFestivalForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            festival = form.save(commit=False)
            festival.vytvoril = request.user
            festival.save()
            messages.success(request, f'Festival {festival.nazov} created')
            # redirect to a new URL:
            return redirect('festivals-show', festival_Id=festival.id)
        else:
            messages.warning(request, f'Check your inputted values!')
            return render(request, 'festivals/new.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        if(not request.user.is_authenticated):
            messages.warning(request, f'Log in to add!')
            return redirect('festivals-home')
        form = NewFestivalForm()
        return render(request, 'festivals/new.html', {'form': form})


def show(request, festival_Id):
    festival = t_festival.objects.get(id=festival_Id)
    try:
        stages = t_stage.objects.filter(festival_id=festival_Id)
    except t_stage.DoesNotExist:
        stages = None
    zucastneni = r_zucastni_sa.objects.filter(id_festival=festival_Id)
    first = True
    query = Q(id=-1)
    for item in zucastneni:
        if first:
            query = Q(id=item.id_interpret.id)
            first = False
        else:
            query.add(Q(id=item.id_interpret.id), Q.OR)
    interprets = t_interpret.objects.filter(query)
    try:
        tickets = t_listok.objects.filter(id_festival=festival_Id)
    except t_listok.DoesNotExist:
        tickets = None
    content = {'festival': festival, 'stages': stages, 'interprets': interprets,
               'tickets': tickets}
    return render(request, 'festivals/show.html', content)


def showStage(request, festival_Id, stage_Id):
    festival = t_festival.objects.get(id=festival_Id)
    stage = t_stage.objects.get(id=stage_Id)
    vystupujuci = r_vystupuje_na.objects.filter(id_stage=stage)
    first = True
    queryPerf = Q(id=-1)
    for item in vystupujuci:
        if first:
            queryPerf = Q(id=item.id_interpret.id)
            first = False
        else:
            queryPerf.add(Q(id=item.id_interpret.id), Q.OR)
    program = zip(t_interpret.objects.filter(queryPerf), vystupujuci)
    return render(request, "festivals/showStage.html", {'program':program, 'stage': stage, 'festival': festival})


def edit(request, festival_Id):
    festival = t_festival.objects.get(id=festival_Id)
    form = NewFestivalForm(instance=festival)
    if request.method == 'POST':
        if(not request.user.is_authenticated):
            messages.warning(request, f'Log in to edit!')
            return render(request, 'festivals/edit.html', {'form': form, 'festival': festival})

        # save owner
        owner = festival.vytvoril
        old_festival = festival

        # create a form instance and populate it with data from the request:
        form = NewFestivalForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            festival = form.save(commit=False)
            festival.vytvoril = owner
            festival.save()
            messages.success(request, f'Festival {festival.nazov} edited')
            old_festival.delete()
            # redirect to a new URL:
            return redirect('festivals-show', festival_Id=festival.id)
        else:
            messages.warning(request, f'Check your inputted values!')
            return render(request, 'festivals/edit.html', {'form': form, 'festival': festival})

        # if a GET (or any other method) we'll create a blank form
    else:
        festival = t_festival.objects.get(id=festival_Id)
        form = NewFestivalForm(instance=festival)
        return render(request, 'festivals/edit.html', {'form': form, 'festival': festival})


def delete(request, festival_Id):
    t_festival.objects.filter(id=festival_Id).delete()
    return redirect('festivals-home')


def addStage(request, festival_Id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewStageForm(request.POST)
        # check whether it's valid:
        festival = get_object_or_404(t_festival, pk=festival_Id)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_stage = form.save(commit=False)
            new_stage.festival_id = festival
            new_stage.save()
            # redirect to a new URL:
            messages.success(request, f'Stage {new_stage.nazov} added.')
            return redirect('festivals-show', festival_Id=festival_Id)
        else:
            return HttpResponse(form)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewStageForm()
        festival = t_festival.objects.get(id=festival_Id)
        return render(request, 'festivals/newStage.html', {'form': form, 'festival': festival})


def editStage(request, stage_Id, festival_Id):
    stage = t_stage.objects.get(id=stage_Id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewStageForm(request.POST, instance=stage)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            messages.success(request, f'Stage changed.')
            return redirect('festivals-show', festival_Id=festival_Id)
        else:
            messages.warning(request, f'Nieco si zle vyplnil.')
            return render(request, 'festivals/editStage.html', {'form': form, 'stage': stage})
    else:
        form = NewStageForm(instance=stage)
        return render(request, 'festivals/editStage.html', {'form': form, 'stage': stage, 'festival_Id': festival_Id})


def deleteStage(request, stage_Id, festival_Id):
    t_stage.objects.get(id=stage_Id).delete()
    return redirect('festivals-show', festival_Id = festival_Id)


def addInterpretToStage(request, stage_Id, interpret_Id, festival_Id):
    festival = t_festival.objects.get(id=festival_Id)
    stage = t_stage.objects.get(id=stage_Id)
    interpret = t_interpret.objects.get(id=interpret_Id)
    if request.method == 'POST':
        programs = r_vystupuje_na.objects.filter(id_stage=stage)
        start_string = request.POST[f'{interpret.nazov}startdate']+" "+request.POST[f'{interpret.nazov}start']+":00+00:00"
        end_string = request.POST[f'{interpret.nazov}enddate']+" "+request.POST[f'{interpret.nazov}end']+":00+00:00"
        print(start_string,end_string)
        starttime = dateutil.parser.parse(start_string)
        endtime = dateutil.parser.parse(end_string)
        # startdate = datetime.datetime.strptime(start_string, "%Y-%m%d %H:%M").datetime()
        # enddate = datetime.datetime.strptime(end_string, "%Y-%m%d %H:%M").datetime()
        for program in programs:
            print(starttime, endtime, program.zaciatok)
            if program.zaciatok<= starttime <= program.koniec or program.zaciatok<= endtime <= program.koniec:
                messages.warning(request, "There is another program at the same time")
                return redirect('festivals-manage-program', festival_Id=festival_Id, stage_Id=stage_Id)
        program = r_vystupuje_na.objects.create(zaciatok=starttime, koniec=endtime, id_stage=stage, id_interpret=interpret)
        messages.success(request, f'Program added.{starttime}')
        return redirect('festivals-manage-program', festival_Id=festival_Id, stage_Id=stage_Id)

    # if a GET (or any other method) we'll create a blank form
    else:
        messages.warning(request, "Rip")
        return redirect('festivals-manage-program', festival_Id=festival_Id, stage_Id=stage_Id)


def manageProgram(request, festival_Id, stage_Id):
    festival = t_festival.objects.get(id=festival_Id)
    zucastneni = r_zucastni_sa.objects.filter(id_festival=festival)
    stage = t_stage.objects.get(id=stage_Id)
    first = True
    query = Q(id=-1)
    for item in zucastneni:
        if first:
            query = Q(id=item.id_interpret.id)
            first = False
        else:
            query.add(Q(id=item.id_interpret.id), Q.OR)
    
    vystupujuci = r_vystupuje_na.objects.filter(id_stage=stage)
    first = True
    queryPerf = Q(id=-1)
    for item in vystupujuci:
        if first:
            queryPerf = Q(id=item.id_interpret.id)
            first = False
        else:
            queryPerf.add(Q(id=item.id_interpret.id), Q.OR)
    performers = zip(t_interpret.objects.filter(queryPerf), vystupujuci)
    interprets = t_interpret.objects.filter(query).exclude(queryPerf)
        
    return render(request, 'festivals/manageStage.html', {'interprets': interprets, 'festival': festival, 'stage': stage, 'performers': performers})


def deleteInterpretFromStage(request, festival_Id, stage_Id, program_Id):
    r_vystupuje_na.objects.get(id=program_Id).delete()
    return redirect('festivals-manage-program', festival_Id=festival_Id, stage_Id=stage_Id)


def editInterpretStage(request, festival_Id, stage_Id, program_Id):
    if request.method == 'POST':
        stage = t_stage.objects.get(id=stage_Id)
        programs = r_vystupuje_na.objects.exclude(id=program_Id).filter(id_stage=stage)
        start_string = request.POST[f'{program_Id}startdate']+" "+request.POST[f'{program_Id}start']+":00+00:00"
        end_string = request.POST[f'{program_Id}enddate']+" "+request.POST[f'{program_Id}end']+":00+00:00"
        starttime = dateutil.parser.parse(start_string)
        endtime = dateutil.parser.parse(end_string)
        for program in programs:
            print(starttime, endtime, program.zaciatok)
            if program.zaciatok<= starttime <= program.koniec or program.zaciatok<= endtime <= program.koniec:
                messages.warning(request, "There is another program at the same time")
                return redirect('festivals-manage-program', festival_Id=festival_Id, stage_Id=stage_Id)
        r_vystupuje_na.objects.filter(id=program_Id).update(zaciatok=starttime, koniec=endtime)
        messages.success(request,"Program updated!")
    return redirect('festivals-manage-program', festival_Id=festival_Id, stage_Id=stage_Id)


def createInterpretFestival(request,festival_Id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewInterpretForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            messages.success(request, f'Interpret created.')
            return redirect('festivals-edit-interprets', festival_Id=festival_Id)
        else:
            messages.warning(request, 'Enter valit data')
            return render(request, 'festivals/createInterpret.html', {'form': form, 'festival_Id': festival_Id})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewInterpretForm()
        return render(request, 'festivals/createInterpret.html', {'form': form, 'festival_Id': festival_Id})


def editInterprets(request, festival_Id):
    festival = t_festival.objects.get(id=festival_Id)
    zucastneni = r_zucastni_sa.objects.filter(id_festival=festival_Id)
    first = True
    query = Q(id=-1)
    for item in zucastneni:
        if first:
            query = Q(id=item.id_interpret.id)
            first = False
        else:
            query.add(Q(id=item.id_interpret.id), Q.OR)
    my_interprets = t_interpret.objects.filter(query)
    interprets = t_interpret.objects.exclude(query)
    if request.method == 'POST':
        interprets = interprets.filter(nazov__contains=request.POST['interpret_name'])
    return render(request, 'festivals/editInterprets.html', {'festival': festival, 'interprets': interprets, 'my_interprets': my_interprets})


def addInterpretToFestival(request, festival_Id, interpret_Id):
    festival = get_object_or_404(t_festival, pk=festival_Id)
    interpret = get_object_or_404(t_interpret, pk=interpret_Id)
    zucastni = r_zucastni_sa()
    zucastni.id_festival = festival
    zucastni.id_interpret = interpret
    zucastni.save()
    return redirect('festivals-edit-interprets', festival_Id=festival_Id)


def deleteInterpretFromFestival(request, festival_Id, interpret_Id):
    r_zucastni_sa.objects.filter(id_festival=festival_Id).filter(id_interpret=interpret_Id).delete()
    return redirect('festivals-edit-interprets', festival_Id= festival_Id)


def showUsers(request):
    user = None
    if(request.method == 'POST'):
        email = request.POST['user_email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f'No user with email \'' + email + '\' found')
            users = User.objects.all()
            return render(request, 'festivals/showUsers.html', {'foundUser': user, 'myUsers': sorted(users, key=operator.attrgetter('last_name'))})

        # user foud
        return redirect('festivals-profile', user_Id=user.id)
    # GET
    else:
        users = User.objects.all()
        return render(request, 'festivals/showUsers.html', {'foundUser': None, 'myUsers': sorted(users, key=operator.attrgetter('last_name'))})


def add_role(request, user_Id, role):
    try:
        user = User.objects.get(id=user_Id)
        group = Group.objects.get(name=role)
    except (User.DoesNotExist, Group.DoesNotExist):
        messages.warning(request, f'Internal error!')
        # users = User.objects.all()
        return redirect('festivals-profile', user_Id=user_Id)

    # user found, assign role
    group.user_set.add(user)

    # user added
    # users = User.objects.all()
    return redirect('festivals-profile', user_Id=user_Id)


def rem_role(request, user_Id, role):
    try:
        user = User.objects.get(id=user_Id)
        group = Group.objects.get(name=role)
    except (User.DoesNotExist, Group.DoesNotExist):
        messages.warning(request, f'Internal error!')
        # users = User.objects.all()
        return redirect('festivals-profile', user_Id=user_Id)

    # user found, assign role
    group.user_set.remove(user)

    # user added
    # users = User.objects.all()
    return redirect('festivals-profile', user_Id=user_Id)


def profile(request, user_Id):
    user = User.objects.get(id=user_Id)
    orders = t_rezervacia.objects.filter(majitel=user).order_by('-id')
    festivals = []
    for order in orders:
        print(order.id)
        reservations = r_rezervacia_na.objects.filter(id_rezervacie=order)
        first = True
        for res in reservations:
            if first:
                print("res :", res.id)
                festivals += [res.id_listku.id_festival]
                first = False
    content=zip(orders, festivals)

    return render(request, 'festivals/profile.html', {'content': content, 'p_user': user})


def editProfile(request, user_Id):
    if(request.method == 'POST'):
        # get user
        pwd = request.POST['password_old']
        new_pwd = request.POST['password_new']
        name = request.POST['name']
        surname = request.POST['surname']

        try:
            user = User.objects.get(id=user_Id)
        except User.DoesNotExist:
            messages.warning(request, f'User not found')
            p_user = User.objects.get(id=user_Id)
            return render(request, 'festivals/editProfile.html', {'p_user': p_user})

        # authenticate user
        if(not (hasher.check_password(pwd, request.user.password) or request.user.groups.filter(name='admin').exists())):
            # auth failed
            if(not hasher.check_password(pwd, request.user.password)):
                messages.warning(request, f'Incorrect password')
            else:
                messages.warning(request, f'You don\'t have permission to edit users')
            p_user = User.objects.get(id=user_Id)
            return render(request, 'festivals/editProfile.html', {'p_user': p_user})

        # save new user data
        user.first_name = name
        user.last_name = surname
        user.additional.display_name = name[0] + ". " + surname
        if(new_pwd != ""):
            user.password = hasher.make_password(new_pwd)

        user.save()
        user.additional.save()

        return redirect('festivals-profile', user_Id=user_Id)
    else:
        p_user = User.objects.get(id=user_Id)
        return render(request, 'festivals/editProfile.html', {'p_user': p_user})


def createTicketFestival(request, festival_Id):
    festival = t_festival.objects.get(id=festival_Id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTicketForm(request.POST)
        # check whether it's valid:
        festival = get_object_or_404(t_festival, pk=festival_Id)
        if form.is_valid():
            try:
                tickets = t_listok.objects.filter(id_festival=festival_Id)
            except t_listok.DoesNotExist:
                tickets = None
            count = 0
            if tickets:
                for ticket in tickets:
                    count += ticket.pocet
            if form.instance.pocet > (festival.kapacita-count):
                messages.warning(request, f'Number of tickets can\'t be bigger than capacity of festival, you can add only {festival.kapacita-count} .')
                return render(request, 'festivals/createTicket.html', {'form': form, 'festival': festival})
            # process the data in form.cleaned_data as required
            new_ticket = form.save(commit=False)
            new_ticket.id_festival = festival
            new_ticket.save()
            # redirect to a new URL:
            messages.success(request, f'Ticket added.')
            return redirect('festivals-show', festival_Id=festival_Id)
        else:
            messages.warning(request, 'Enter valit data')
            return render(request, 'festivals/createTicket.html', {'form': form, 'festival': festival})
        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTicketForm()
        return render(request, 'festivals/createTicket.html', {'form': form, 'festival': festival})


def editTicketFestival(request, festival_Id, ticket_Id):
    ticket = t_listok.objects.get(id=ticket_Id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewTicketForm(request.POST, instance=ticket)
        # check whether it's valid:
        festival = get_object_or_404(t_festival, pk=festival_Id)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_ticket = form.save(commit=False)
            new_ticket.id_festival = festival
            new_ticket.save()
            # redirect to a new URL:
            messages.success(request, f'Ticket added.')
            return redirect('festivals-show', festival_Id=festival_Id)
        else:
            return HttpResponse(form)
        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewTicketForm(instance=ticket)
        festival = t_festival.objects.get(id=festival_Id)
        return render(request, 'festivals/edit.html', {'form': form, 'festival': festival})


def buyTicketPage(request, festival_Id):
    myfestival = t_festival.objects.get(id=festival_Id)
    try:
        tickets = t_listok.objects.filter(id_festival=festival_Id)
    except t_listok.DoesNotExist:
            tickets = None
    count = []
    for ticket in tickets:
        count += [ticket.pocet - r_rezervacia_na.objects.filter(id_listku=ticket).count()]
    content = zip(tickets, count)
    if request.method == 'POST':
        if request.user.is_authenticated:
            reservation = t_rezervacia.objects.create(stav="reserved", email=request.user.email, majitel=request.user)
            reservation.save()
            #reservation = get_object_or_404(t_rezervacia, pk= reservation.id)
            for ticket in tickets:
                count = r_rezervacia_na.objects.filter(id_listku=ticket.id).count()
                numOfTickets = int(request.POST[ticket.typ])
                if ticket.pocet-count < numOfTickets:
                    messages.warning(request, f"There is only  {ticket.pocet-count} {ticket.typ}tickets left")
                    reservation.delete()
                    return render(request, 'festivals/tickets.html', {'festival': myfestival, 'tickets': content})
                for i in range(numOfTickets):
                    print("vytvaram",reservation.id)
                    temp = r_rezervacia_na.objects.create(id_rezervacie=reservation, id_listku=ticket)
                    temp.save()
            messages.success(request,"Tickets added to your reservations")
            return redirect('festivals-show', festival_Id=festival_Id)
        else:
            reservation = t_rezervacia.objects.create(stav="reserved", email=request.POST['email'])
            reservation.save()
            reservation = get_object_or_404(t_rezervacia, pk= reservation.id)
            for ticket in tickets:
                count = r_rezervacia_na.objects.filter(id_listku=ticket).count()
                if ticket.pocet-count < int(request.POST[ticket.typ]):
                    messages.warning(request, f"There is only  {ticket.pocet-count} {ticket.typ}tickets left")
                    reservation.delete()
                    return render(request, 'festivals/tickets.html', {'festival': myfestival, 'tickets': content})
                for i in range(int(request.POST[ticket.typ])):
                    temp = r_rezervacia_na.objects.create(id_rezervacie=reservation, id_listku=ticket)
                    temp.save()
            messages.success(request,"Tickets added to your reservations")
            return redirect('festivals-show', festival_Id=festival_Id)
    else:
        return render(request, 'festivals/tickets.html', {'festival': myfestival, 'tickets': content})


def showReservation(request, res_Id, festival_Id):
    festival = t_festival.objects.get(id=festival_Id)
    tickets = t_listok.objects.filter(id_festival=festival)
    reservation = t_rezervacia.objects.get(id=res_Id)
    count = []
    price = 0
    for ticket in tickets:
        numOfTickets = r_rezervacia_na.objects.filter(id_listku=ticket).filter(id_rezervacie=reservation).count()
        count += [numOfTickets]
        price += numOfTickets*ticket.cena
    tickets = zip(tickets, count)
    content = {'tickets': tickets, 'festival': festival, 'reservation': reservation, 'price': price}
    return render(request, 'festivals/reservation.html', content)


def payReservation(request, res_Id):
    reservation = t_rezervacia.objects.get(id=res_Id)
    reservation.stav = "Wainting for approval"
    reservation.save()
    user_Id = reservation.majitel.id
    return render(request,"festivals/pay.html", {'owner_Id': user_Id})

def deleteReservation(request, res_Id):
    t_rezervacia.objects.get(id=res_Id).delete()
    messages.success(request, "Reservation canceled")
    return redirect('festivals-profile')


def confirmReservation(request, res_Id):
    reservation = t_rezervacia.objects.get(id=res_Id)
    reservation.stav = "Ready to pick up"
    reservation.save()
    return redirect('festivals-profile')

def completeReservation(request, res_Id):
    reservation = t_rezervacia.objects.get(id=res_Id)
    reservation.stav = "Completed"
    reservation.save()
    return redirect('festivals-profile')


def showInterprets(request):
    interprets = t_interpret.objects.all()
    if request.method == 'POST':
        interprets = interprets.filter(nazov__contains=request.POST['interpret_name'])
    return render(request, 'festivals/showInterprets.html', {'interprets': interprets})

def interpretProfile(request, interpret_Id):
    interpret = t_interpret.objects.get(id=interpret_Id)
    zucastneni = r_zucastni_sa.objects.filter(id_interpret=interpret)
    first = True
    query = Q(id=-1)
    for item in zucastneni:
        if first:
            query = Q(id=item.id_festival.id)
            first = False
        else:
            query.add(Q(id=item.id_festival.id), Q.OR)
    Content = {'festivals': t_festival.objects.filter(query).filter(zaciatok__gte=datetime.date.today()), 'interpret':interpret}
    return render(request, "festivals/interpretProfile.html", Content)


def createInterpret(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewInterpretForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            messages.success(request, f'Interpret created.')
            return redirect('interprets-show')
        else:
            messages.warning(request, 'Enter valit data')
            return render(request, 'festivals/createInterprets.html', {'form': form})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewInterpretForm()
        return render(request, 'festivals/createInterprets.html', {'form': form})