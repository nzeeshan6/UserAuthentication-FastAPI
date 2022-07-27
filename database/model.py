from deta import Deta

deta = Deta()
User = deta.Base('User-Creds')
activeUser = deta.Base('active_Sess')

    