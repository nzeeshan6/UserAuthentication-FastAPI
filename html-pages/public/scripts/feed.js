let logOut = document.getElementById('logout')
        logOut.addEventListener('click', ()=>{
            console.log('Button Clicked')
            logOut.innerHTML = 'Logging Out..'
            fetch('/logout',{
                method:'POST',
                redirect:'follow'
            }).then(response=>{response.json()
                if (response.redirected){
                    window.location.href = response.url;
                }}).done()
        })

        let username = document.getElementById('userName')
        let feedError = document.getElementById('feedError')

        let data = fetch('/feed', {method: 'Post', redirect:'follow'})

        let realdata = data.then((response)=>{
            if (response.redirected){
                window.location.href = response.url
            }
            return response.json()
        })

        realdata.then((d)=>{
            console.log(d)
            var name = d.name
            var error = d.error
            if (name){
                document.title= `${name}- Feed`
                username.innerHTML = name
            }
            else{
                feedError.innerHTML = error
            }
        })