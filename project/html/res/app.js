(function() {
    const unloggedLinks = {
        "Home":"home.html",
        "Login":"login.html",
        "Register":"register.html",
    }

    const loggedLinks = {
        "Home":"home.html",
        "Profile":"profile.html",
        "Transfer":"transfer.html",
    }

    function displayLinks() {
        let output = ""
        const links = (document.cookie.includes('mb_session_id') ? loggedLinks : unloggedLinks)
        console.log(links)
        for (let link in links) {
            output += `<a onclick="app.loadPartial('${links[link]}')">${link}</a>`
        }
        document.getElementById('links').innerHTML = output
    }

    function loadPartial(partial) {
        console.log('loadPartial :: ', partial)
        let req = new XMLHttpRequest();
        req.onload = applyPartial;
        req.open("get", `/partials/${partial}`, true);
        req.send();
    }

    function applyPartial() {
        document.getElementById('container').innerHTML = this.responseText;
    }

    function init() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('view')) {
            loadPartial(urlParams.get('view')+'.html')
        } else {
            loadPartial('home.html')
        }
        console.log('app.js initialized')
        displayLinks()
        if (urlParams.has('error')) {
            document.getElementById('error').innerHTML = urlParams.get('error')
            document.getElementById('error').style.display = 'block'
        } else if (urlParams.has('message')) {
            document.getElementById('message').innerHTML = urlParams.get('message')
            document.getElementById('message').style.display = 'block'
        }
    }

    window.app = {init, loadPartial}

    document.onreadystatechange = () => {
        app.init()
    }
})();