function render(){
    var loginButton = document.getElementById('login');
    var registerButton = document.getElementById('register');
    var registerForm = document.getElementById('registrationForm');
    var loginForm = document.getElementById('loginForm');

    loginForm.style.display = loginButton.checked ? "Block" : "none";
    registerForm.style.display = registerButton.checked ? "Block" : "none";

}
function authRegister(){
    // console.log('Register Window');
    let nameError = document.getElementById('nameError');
    let emailError = document.getElementById('emailError');
    let pwdError = document.getElementById('pwdError');
    nameError.innerHTML = "";
    emailError.innerHTML = "";
    pwdError.innerHTML = "";

    let fname = document.getElementById('fName');
    let lname = document.getElementById('lName');
    let mail = document.getElementById('email');
    let pass = document.getElementById('newCode');
    let vpass = document.getElementById('verifyCode');

    if (fname.value.match(/^[A-Za-z]+$/) && lname.value.match(/^[A-Za-z]+$/)){
        var mailformat = /^[A-Za-z@.0-9]+$/;
        if (mail.value.match(mailformat)){
            if (pass.value.length >=8){
                if (pass.value == vpass.value){
                    // Everything validated
                    fetch('/register', {
                        method:'Post',
                        redirect:'follow',
                        body: JSON.stringify({
                            name: fname.value+' '+lname.value,
                            email: mail.value,
                            password: pass.value
                        }),
                        headers:{'content-type':'application/json'
                        }
                    }).then(response=>{
                        if (response.redirected) {
                            window.location.href = response.url;
                        }
                        if (response.status==409){
                            emailError.innerHTML = 'User Already Exists!! Please Sign-In'
                        }
                        response.json()})
                    .then((json)=>{
                        console.log(json)
                    })
                }
                else{
                    pwdError.innerHTML = 'Passwords do not match';
                    pass.focus();
                }
            }
            else{
                pwdError.innerHTML = 'Password too Short';
                pass.focus();
            }
        }
        else{
            emailError.innerHTML = "Invalid E- Mail";
            email.focus();
        }
    }
    else{
        //name error
        nameError.innerHTML="Invalid Name";
        fname.focus();
    }
}

function authLogin(){
    // console.log('Login Window');
    let mail = document.getElementById('userName');
    let passwrd = document.getElementById('passwrd');
    let loginError = document.getElementById('loginError');
    loginError.innerHTML = "";
    var mailformat = /^[A-Za-z@.0-9]+$/;

    if (mail.value.match(mailformat) && passwrd.value.length>=8){
        fetch('/login',{
            method:'Post',
            redirect:'follow',
            body:JSON.stringify({
                email: mail.value,
                password: passwrd.value
            }),
            headers:{
                'content-type':'application/json'
            }
        }).then(response=>{
            if (response.redirected) {
                window.location.href = response.url;
            }
            if (response.status == 404){
                loginError.innerHTML = "User Not Found!! Please Register"
            }
            if (response.status == 400){
                loginError.innerHTML = "Invalid Credentials"
            }
            response.json()
        })
        .then((json)=>{
            console.log(json);
        })
    }
    else{
        loginError.innerHTML = "Invalid Credentials";
        email.focus();
    }
}


let registerSubmit = document.getElementById('submitRegister');
let loginSubmit = document.getElementById('submitLogin');
loginSubmit.addEventListener('submit',(event)=>{
    event.preventDefault();
    authLogin();
})
registerSubmit.addEventListener('submit', (event)=>{
    event.preventDefault();
    authRegister();
})