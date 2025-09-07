


def detectuser(user):
    if user.role == 1:
        redirecturl = 'sellerdashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'customerdashboard'
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
        return redirecturl
    





