from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = []
            if request.user.groups.exists():
                # Use this to filter out the user's permission group
                group = [i.name for i in request.user.groups.all()]

                # OR use this to do same:
                # group = request.user.groups.all()[0].name
            
            # The 'if' statement below is use to compare the user's
            #..permission group with the permission provided in the view
            #..function.
            if all(item in group for item in allowed_roles):
            # if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view the page')
        return wrapper_func
    return decorator