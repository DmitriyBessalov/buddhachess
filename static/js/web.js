const AlertMDB = (text, color) => {
  let a_color = 'alert-secondary' // purple
  if (color === 'green') a_color = 'alert-success'
  if (color === 'red') a_color = 'alert-danger'
  let alert = document.createElement("div")
  document.querySelector('body').appendChild(alert)
  alert.outerHTML = '\
  <div class="alert mb-0 alert-dismissible alert-absolute fade show alert-fixed ' + a_color + '"\
       role="alert" data-mdb-color="secondary"\
       style="width: 360px; top: 70px; right: 20px; transform: unset;">\
       ' + text + '\
    <button type="button" class="btn-close ms-2" data-mdb-dismiss="alert" aria-label="Close"></button>\
  </div>'
}

let access_token

async function auth_session() {
  let
    response,
    user
  if (sessionStorage.getItem("username") !== null) {
    if (localStorage.getItem("access_token") !== null) {
      access_token = localStorage.getItem("access_token")
    } else {
      access_token = localStorage.getItem("anonimous_access_token")
    }
  } else {
    if (localStorage.getItem("access_token") === null) {
      response = await fetch('/api/auth/create_anonimous_token?token='+localStorage.getItem("anonimous_access_token"))
    } else {
      response = await fetch('/api/auth/me',
        {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        }
      )
    }
    // console.log(await response)
    user = await response.json()
    if (user.detail !== undefined) {
      localStorage.removeItem("access_token")
      auth_session()
    } else {
      sessionStorage.setItem("username", user.username)
      console.log(user)
      if (user.access_token !== undefined) {
        localStorage.setItem("access_token", user.access_token)
        access_token = user.access_token
      }
      if (user.access_token_anonimous !== undefined) {
        localStorage.setItem("access_token_anonimous", user.access_token_anonimous)
        access_token = user.access_token_anonimous
      }
    }
  }
}