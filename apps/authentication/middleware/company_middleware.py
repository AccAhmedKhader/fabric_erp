import logging

logger = logging.getLogger(__name__)

class CompanyContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.path.startswith('/admin/'):
            if not request.user.is_superuser:
                if not request.session.get('current_company_id'):
                    user_companies = request.user.user_companies.all()
                    if user_companies.exists():
                        default_company = user_companies.filter(is_default=True).first()
                        if default_company:
                            request.session['current_company_id'] = str(default_company.company_id)
                        else:
                            request.session['current_company_id'] = str(user_companies.first().company_id)

        response = self.get_response(request)
        return response