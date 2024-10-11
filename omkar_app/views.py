# booking/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
import razorpay
from .forms import CoupleRoomForm, FamilyRoomForm, GroupRoomForm, DormitoryForm, SixBedRoomForm
from .models import Couple_Room, Family_Room, Group_Room, Six_Bed_Room, Dormitory
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from twilio.rest import Client




def home(request):
    return render(request,'home.html')


def background(request):
    return render(request,'background.html')


def payment_options(request):
    return render(request, 'payment_options.html')


def cash_payment(request, booking_id, room_type):
    # Get the booking object to retrieve name and phone number
    if room_type == 'couple':
        booking = get_object_or_404(Couple_Room, id=booking_id)
    elif room_type == 'family':
        booking = get_object_or_404(Family_Room, id=booking_id)
    elif room_type == 'group':
        booking = get_object_or_404(Group_Room, id=booking_id)
    elif room_type == 'sixbed':
        booking = get_object_or_404(Six_Bed_Room, id=booking_id)
    elif room_type == 'dormitory':
        booking = get_object_or_404(Dormitory, id=booking_id)
    else:
        return redirect('not_available')  # In case of an invalid room type

    # Prepare email content for cash payment
    subject = f"Cash Payment Confirmation for {room_type.capitalize()} Room"
    message = (f'''
               Booking Details:
               Name: {booking.Name}
               Phone: {booking.Phone}
               Room Type: {room_type.capitalize()}
               ''')

    recipient_email = 'quickstudywithanju@gmail.com'  # Your recipient email

    # Send the email
    send_mail(subject, message, 'adarshrajstest@gmail.com', [recipient_email], fail_silently=False)

    return render(request, 'cash_booking_confirmed.html')


# booking/views.py


def online_payment(request):
    if request.method == 'POST':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': 1000, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'razorpay_payment.html', {'payment': payment})

    return render(request, 'razorpay_payment.html')


def payment_success(request):
    payment_id = request.GET.get('payment_id')
    # Process the payment_id as needed (e.g., store it in the database)

    # Get the booking details based on the payment_id (you may need to implement a lookup)
    # For simplicity, I'll assume you have a way to retrieve booking_id from payment details.
    booking_id = ...  # Add your logic to get booking_id based on payment_id

    # Now get the booking object
    booking = get_object_or_404(Couple_Room, id=booking_id)  # Change this to the correct model

    # Prepare email content for online payment
    subject = f"Online Payment Confirmation for {booking.Room_type.capitalize()} Room"
    message = (f'''
               Booking Details:
               Name: {booking.Name}
               Phone: {booking.Phone}
               Room Type: {booking.Room_type.capitalize()}
               ''')

    recipient_email = 'quickstudywithanju@gmail.com'  # Your recipient email

    # Send the email
    send_mail(subject, message, 'adarshrajstest@gmail.com', [recipient_email], fail_silently=False)

    return render(request, 'payment_success.html', {'payment_id': payment_id})


def not_available(request):
    return render(request,'not_available.html')



def book_couple_room(request):
    if request.method == 'POST':
        form = CoupleRoomForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save the form data
            # Redirect to the view where users can confirm the booking details
            return redirect('view-booking-details', booking_id=booking.id, room_type='couple')
    else:
        form = CoupleRoomForm()

    return render(request, 'Couple.html', {'form': form})


def book_Family_room(request):
    if request.method == 'POST':
        form = FamilyRoomForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save the form data to the FamilyRoom model
            return redirect('view-booking-details', booking_id=booking.id, room_type='family')
    else:
        form = FamilyRoomForm()

    return render(request, 'Family.html', {'form': form})


def book_Group_room(request):
    if request.method == 'POST':
        form = GroupRoomForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save the form data to the GroupRoom model
            return redirect('view-booking-details', booking_id=booking.id, room_type='group')
    else:
        form = GroupRoomForm()

    return render(request, 'Group.html', {'form': form})


def book_Six_room(request):
    if request.method == 'POST':
        form = SixBedRoomForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save the form data to the SixBedRoom model
            return redirect('view-booking-details', booking_id=booking.id, room_type='sixbed')
    else:
        form = SixBedRoomForm()

    return render(request, 'Sixbed.html', {'form': form})


def book_Dormitory(request):
    if request.method == 'POST':
        form = DormitoryForm(request.POST)
        if form.is_valid():
            booking = form.save()  # Save the form data to the Dormitory model
            return redirect('view-booking-details', booking_id=booking.id, room_type='dormitory')
    else:
        form = DormitoryForm()

    return render(request, 'Dormitory.html', {'form': form})



def view_booking_details(request, booking_id, room_type):
    # Get the booking object based on the room_type and booking_id
    if room_type == 'couple':
        booking = get_object_or_404(Couple_Room, id=booking_id)
        form_class = CoupleRoomForm
        redirect_url = 'book_couple_room'
    elif room_type == 'family':
        booking = get_object_or_404(Family_Room, id=booking_id)
        form_class = FamilyRoomForm
        redirect_url = 'book_Family_room'
    elif room_type == 'group':
        booking = get_object_or_404(Group_Room, id=booking_id)
        form_class = GroupRoomForm
        redirect_url = 'book_Group_room'
    elif room_type == 'sixbed':
        booking = get_object_or_404(Six_Bed_Room, id=booking_id)
        form_class = SixBedRoomForm
        redirect_url = 'book_Six_room'
    elif room_type == 'dormitory':
        booking = get_object_or_404(Dormitory, id=booking_id)
        form_class = DormitoryForm
        redirect_url = 'book_Dormitory'
    else:
        return redirect('not_available')  # In case of an invalid room type

    # Render the form with the booking data
    form = form_class(instance=booking)

    # Make form read-only
    for field in form.fields:
        form.fields[field].widget.attrs['disabled'] = True

    if request.method == 'POST':
        if 'ok' in request.POST:
            return redirect('booking-success',booking_id=booking_id,room_type=room_type)
        elif 'cancel' in request.POST:
            return redirect(redirect_url)

    return render(request, 'view_booking_details.html',{'form': form, 'booking_id': booking_id, 'room_type': room_type})



def booking_success(request, booking_id, room_type):
    global booking
    # Retrieve the booking object based on room type
    if room_type == 'couple':
        booking = get_object_or_404(Couple_Room, id=booking_id)
    elif room_type == 'family':
        booking = get_object_or_404(Family_Room, id=booking_id)
    elif room_type == 'group':
        booking = get_object_or_404(Group_Room, id=booking_id)
    elif room_type == 'sixbed':
        booking = get_object_or_404(Six_Bed_Room, id=booking_id)
    elif room_type == 'dormitory':
        booking = get_object_or_404(Dormitory, id=booking_id)

    # Prepare email content
    subject = f"Booking Confirmation for {room_type.capitalize()} Room"
    message = (f'''
               Details:
               Room Type: {room_type.capitalize()}
               Room Name: {booking.Room_name} 
               Room Amount: {booking.Room_amount}
               Check-in: {booking.Check_in}
               Check-out: {booking.Check_out}
               Name: {booking.Name}
               Phone: {booking.Phone}
               Email: {booking.Email}
               Adults: {booking.Adults}
               Child: {booking.Child}              
               ''')
    recipient_email = 'quickstudywithanju@gmail.com'

    # Send the email
    send_mail(subject, message, 'adarshrajstest@gmail.com', [recipient_email], fail_silently=False)

    # Send WhatsApp message (your existing logic)

    return render(request, 'booking_success.html', {
        'booking': booking,
        'booking_id': booking_id,
        'room_type': room_type
    })









