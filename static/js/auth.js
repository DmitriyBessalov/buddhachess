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

authForm.onsubmit = async (e) => {
  e.preventDefault()
  const
    data = new FormData(e.target),
    value = Object.fromEntries(data.entries()),
    action = authForm.action.replace(window.location.origin + '/api/auth/', '')

  let
    response,
    form_valid = true

  if (action === 'token')
    response = await fetch(e.path[0].action, {
      method: e.path[0].method,
      body: new FormData(authForm)
    })
  else
    response = await fetch(e.path[0].action, {
      method: e.path[0].method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      },
      body: JSON.stringify(value)
    })

  console.log(await response)
  const result = await response.json()

  for (const prop in value) {
    let input = document.querySelector('[name=' + prop + ']')
    if (result?.detail?.[0]?.loc?.[1] === prop) {
      // input.classList.remove('is-valid')
      input.classList.add('is-invalid')
      let msg = document.querySelector('[name=' + prop + ']~.invalid-feedback')
      msg.innerHTML = result.detail[0].msg
      form_valid = false
    } else {
      // input.classList.add('is-valid')
      input.classList.remove('is-invalid')
    }
  }
  if (form_valid) {
    authForm.querySelector('button[type=submit]').disabled = true
    switch (action) {
      case 'register':
        AlertMDB("Вы успешно зарегистрировались! Вам отправлено письмо на email. Подтвердите вашу почту", "green")
        break
      case 'token':
        localStorage.setItem('username', result.username)
        localStorage.setItem('access_token', result.access_token)
        if (loginCheck.checked) {
          localStorage.setItem('password', value.password)
        }
        AlertMDB("Вы успешно авторизовались!", "green")
        break
      case 'password':
        console.log('password')
        break
      case 'reset_password':
        AlertMDB("Письмо отправленно на email", "green")
        break
      case 'password_confirm':
        AlertMDB("Пароль успешно изменён", "green")
    }
  }
}
