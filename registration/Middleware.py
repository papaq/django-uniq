from django.shortcuts import redirect


class AuthRequiredMiddleware(object):

    @staticmethod
    def process_request(request):
        if not request.user.is_authenticated():
            return redirect('registration:register')
        return None
