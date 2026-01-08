from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import ChatThread, Message, BlockedUser
from listings.models import Listing
import json

User = get_user_model()

@login_required
def chat_list(request):
    # Get all chats where user is buyer or seller
    chats = ChatThread.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user),
        is_active=True
    ).select_related('listing', 'buyer', 'seller').prefetch_related('messages')
    
    # Add unread status to each chat
    chats_with_unread = []
    for chat in chats:
        chat.has_unread_messages = chat.has_unread(request.user)
        chats_with_unread.append(chat)
    
    context = {
        'chats': chats_with_unread,
    }
    return render(request, 'chat/chat_list.html', context)

@login_required
def chat_detail(request, thread_id):
    thread = get_object_or_404(
        ChatThread.objects.filter(
            Q(buyer=request.user) | Q(seller=request.user),
            id=thread_id
        )
    )
    
    # Mark messages as read
    thread.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    # Get chat messages
    messages = thread.messages.all().order_by('sent_at')
    
    context = {
        'thread': thread,
        'messages': messages,
        'other_user': thread.seller if request.user == thread.buyer else thread.buyer,
    }
    return render(request, 'chat/chat_detail.html', context)

@login_required
def start_chat(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_active=True)
    
    if request.user == listing.seller:
        messages.error(request, "You cannot chat with yourself!")
        return redirect('listing_detail', listing_id=listing_id)
    
    # Check if chat already exists
    thread, created = ChatThread.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        seller=listing.seller,
        defaults={'is_active': True}
    )
    
    if created:
        messages.success(request, "Chat started! Send a message to the seller.")
    
    return redirect('chat_detail', thread_id=thread.id)

@login_required
@csrf_exempt
def send_message(request, thread_id):
    if request.method == 'POST':
        thread = get_object_or_404(
            ChatThread.objects.filter(
                Q(buyer=request.user) | Q(seller=request.user),
                id=thread_id
            )
        )
        
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        image = request.FILES.get('image')
        
        if content or image:
            message = Message.objects.create(
                thread=thread,
                sender=request.user,
                content=content,
                image=image
            )
            
            # Update thread's updated_at
            thread.save()
            
            return JsonResponse({
                'success': True,
                'message_id': str(message.id),
                'content': message.content,
                'image_url': message.image.url if message.image else None,
                'sender': message.sender.username,
                'sent_at': message.sent_at.isoformat(),
            })
        
        return JsonResponse({'success': False, 'error': 'Empty message'})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})

@login_required
def get_messages(request, thread_id):
    thread = get_object_or_404(
        ChatThread.objects.filter(
            Q(buyer=request.user) | Q(seller=request.user),
            id=thread_id
        )
    )
    
    last_message_id = request.GET.get('last_message_id')
    
    if last_message_id:
        messages = thread.messages.filter(id__gt=last_message_id)
    else:
        messages = thread.messages.all().order_by('-sent_at')[:50]
    
    messages_data = []
    for msg in messages:
        messages_data.append({
            'id': str(msg.id),
            'sender': msg.sender.username,
            'content': msg.content,
            'image_url': msg.image.url if msg.image else None,
            'is_read': msg.is_read,
            'sent_at': msg.sent_at.isoformat(),
        })
    
    return JsonResponse({'messages': messages_data})

@login_required
def block_user(request, user_id):
    user_to_block = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Check if already blocked
        if BlockedUser.objects.filter(blocker=request.user, blocked=user_to_block).exists():
            messages.warning(request, "User is already blocked.")
        else:
            BlockedUser.objects.create(
                blocker=request.user,
                blocked=user_to_block,
                reason=request.POST.get('reason', '')
            )
            messages.success(request, f"{user_to_block.username} has been blocked.")
        
        return redirect('dashboard')
    
    return render(request, 'chat/block_user.html', {'user_to_block': user_to_block})
