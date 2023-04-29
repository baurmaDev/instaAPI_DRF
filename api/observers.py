from django.core.mail import send_mail

class NewPostNotification:
    def update(self, sender, post, **kwargs):
        print("Email has been send ")
        # subject = f"New post by {post.user.user.username}"
        # message = f"Hello,\n\nA new post has been created by {post.user.user.username}.\n\nCaption: {post.caption}\n\nThanks!"
        # from_email = "admin@example.com"
        # recipient_list = ["user1@example.com", "user2@example.com"]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
