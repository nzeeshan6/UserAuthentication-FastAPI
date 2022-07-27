from fastapi import APIRouter, status, Depends, HTTPException, Response, Request
from fastapi.responses import FileResponse, RedirectResponse
from database import schema, crypto, token
from database.model import activeUser, User
COOKIE_KEY = 'c2cf459eb42cdb21572753ce4026b8106c2ee673e778e8d60fa8d312079a3686'

router = APIRouter(
    tags=['User']
)


@router.get('/')
def index(request: Request, response:Response):
    for i in range(0,5):
        requestToken = request.cookies.get(COOKIE_KEY)
        print('Requesting Resume')
        if requestToken:
            break

    if requestToken: 
        # check for token validity
        auth = token.validate_access_token(requestToken)

        if auth=='404' or auth=='307':
            response = FileResponse('./html-pages/index.html')
            response.delete_cookie(COOKIE_KEY, httponly=True)
            return response
        else:
            response = RedirectResponse('/feed', status_code=status.HTTP_302_FOUND)
            return response
    else:
        return FileResponse('./html-pages/index.html')


@router.get('/feed')
def dashboard(request: Request, response:Response):
    for i in range(0,5):
        requestToken = request.cookies.get(COOKIE_KEY, '/')
        if requestToken:
            break

    if requestToken: 
        # check for token validity
        auth = token.validate_access_token(requestToken)

        if auth=='404' or auth=='307':
            response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
            response.delete_cookie(COOKIE_KEY, httponly=True)
            return response
        else:
            response = FileResponse('./html-pages/feed.html')
            return response
    else:
        return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@router.post('/login', status_code=status.HTTP_200_OK)
def login(req: schema.Login, response: Response):
    result = User.fetch({"email":req.email})
    print(result.count)
    if result.count == 0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='User Not Found')
    else:
        if not crypto.verify(req.password, result.items[0].get('password')):
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='Invalid Credentials')
        else:
            access_token = token.create_access_token(
                data={"sub": req.email}
            )
            print('token generated')

            token.store_access_token(access_token, req.email)
            print('token stored')

            response = RedirectResponse('/feed', status_code=status.HTTP_302_FOUND)
            response.set_cookie(key=COOKIE_KEY, value = access_token, httponly=True)
            return response


@router.post('/register', status_code=status.HTTP_200_OK)
def create_user(req: schema.User):
    result = User.fetch({'email': req.email})
    if result.count>0:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User Already Exists')
    hashedPwd = crypto.encrypt(req.password)
    req.password = hashedPwd
    User.put(req.dict())
    return RedirectResponse('/',status_code = status.HTTP_302_FOUND)


@router.post('/logout', status_code=status.HTTP_200_OK)
def logout( response : Response):
    response = RedirectResponse('/', status_code = status.HTTP_302_FOUND)
    response.delete_cookie(COOKIE_KEY, httponly=True)
    return response


@router.post('/feed', status_code= status.HTTP_200_OK,response_model=schema.UserFeed)
def getFeed(request: Request, response:Response):
    for i in range(0,5):
        requestToken = request.cookies.get(COOKIE_KEY, '/')
        if requestToken:
            break
    
    if (requestToken):
        auth = token.validate_access_token(requestToken)
        if auth=='404' or auth=='307':
            response = {'name':None, 'error':'Invalid Token Please Try Again'}
            response.delete_cookie(COOKIE_KEY)
            return response
        else:
            result = User.fetch({'email':auth})
            if (result.count>0):
                return result.items[0]
            else:
                response = {'name':None, 'error':'User Not Found Please Register'}
                return response
    else:
        response = {'name':None, 'error':'Invalid Token Please Try Again'}
        return response