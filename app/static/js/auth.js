authForm.onsubmit = async (e) => {
  e.preventDefault()
  const
    data = new FormData(e.target),
    value = Object.fromEntries(data.entries()),
    action = authForm.action.replace(window.location.origin + '/api/auth/', '')

  let
    response,
    form_valid = true

    console.log(JSON.stringify(value))

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
