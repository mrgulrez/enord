# from django.http import JsonResponse
# from UserServices.models import ModuleUrls, UserPermissions
# from rest_framework_simplejwt.authentication import JWTAuthentication
# import re
# from django.db.models import Q

# class PermissionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
        
#         current_url = request.path
#         if current_url in urlToSkip():
#             return response
        
#         jwt_auth=JWTAuthentication()
#         try:
#             user,token=jwt_auth.authenticate(request)
#             if not user:
#                 return JsonResponse({'message':'Unauthorized'},status=401)
#         except:
#             return JsonResponse({'message':'Unauthorized'},status=401)
        
#         # Skip Permission Logic for Super Admin and Top Domain Level User
#         if user.role=='Super Admin' or user.domain_user_id.id==user.id:
#             return response

#         module=find_matching_module(current_url)
        
#         if not module:
#             return JsonResponse({'message':'Module not Exist'},status=400)
        

#         permission=UserPermissions.objects.filter(user=user.id,module=module.module).first()
#         if not permission or permission.is_permission==False:
#             return JsonResponse({'message':'Permission Denied'},status=403)
        

#         return response
    

# def urlToSkip():
#     modules=ModuleUrls.objects.filter(module__isnull=True).values_list('url',flat=True)
#     return modules

# def find_matching_module(url):
#     regex_pattern=re.sub(r'\d+','[^\/]+',url.replace('/','\/'))

#     match_patter=ModuleUrls.objects.filter(Q(url__iregex=f'^{regex_pattern}$')).first()
#     return match_patter




# EcommerceInventory/middleware/PermissionMiddleware.py

from django.http import JsonResponse
from UserServices.models import ModuleUrls, UserPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import re

# * Add any other paths you want completely public *
PUBLIC_PATH_PREFIXES = [
    '/',                 # root index.html
    '/favicon.ico',      # browser icon
    settings.STATIC_URL, # e.g. '/static/'
    '/api/auth/',        # signup/login
]

def urlToSkip():
    # also include any ModuleUrls entries (your dynamic form URLs, file uploads, etc.)
    urls_from_db = list(ModuleUrls.objects.filter(module__isnull=True).values_list('url', flat=True))
    return PUBLIC_PATH_PREFIXES + urls_from_db



def find_matching_module(url):
    regex_pattern = re.sub(r'\d+', '[^\\/]+', url.replace('/', '\\/'))
    return ModuleUrls.objects.filter(url__iregex=f'^{regex_pattern}$').first()

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # 1) Quick-pass public paths & static files
        for prefix in urlToSkip():
            if path.startswith(prefix):
                return self.get_response(request)

        # 2) Authenticate JWT
        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
            if not user:
                raise Exception()
        except:
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        # 3) Super‑Admin / domain‑owner bypass
        if user.role == 'Super Admin' or user.domain_user_id_id == user.id:
            return self.get_response(request)

        # 4) Find module metadata for this path
        module = find_matching_module(path)
        if not module:
            return JsonResponse({'message': 'Module not Exist'}, status=400)

        # 5) Check permission record
        perm = UserPermissions.objects.filter(user=user.id, module=module.module).first()
        if not perm or not perm.is_permission:
            return JsonResponse({'message': 'Permission Denied'}, status=403)

        return self.get_response(request)
