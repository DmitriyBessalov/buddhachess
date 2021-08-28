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

const form = document.querySelector('.needs-validation.auth')
form.addEventListener('submit', function (event) {
  event.preventDefault()
  const data = new FormData(event.target)
  const value = Object.fromEntries(data.entries())

  fetch(event.path[0].action, {
    method: event.path[0].method,
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(value)
  }).then(
    async response => ({
      status: response.status,
      body: await response.text(),
    })
  ).then(
    response => {
      console.log(response.body)
      response = JSON.parse(response.body)
      let form_valid = true

        for (const prop in value) {
          let input = document.querySelector('[name=' + prop + ']')
          if ((typeof (response.detail) != "undefined") && (response.detail[0].loc[1] === prop))  {
            // input.classList.remove('is-valid')
            input.classList.add('is-invalid')
            let msg = document.querySelector('[name=' + prop + ']~.invalid-feedback')
            msg.innerHTML = response.detail[0].msg
            form_valid = false
          } else {
            // input.classList.add('is-valid')
            input.classList.remove('is-invalid')
          }
      }
      if (form_valid) {
        form.querySelector('button[type=submit]').disabled = true
        form_action(response, form.action)
      }
    }
  )
})


form_action = (response, action) => {
  action = action.replace(window.location.origin + '/api/auth/', '')
  switch (action.slice(0, -1)) {
    case 'register':
      AlertMDB("Вы успешно зарегистрировались! Теперь подтвердите ваш email, Вам отправлено письмо", "green")
      break
    case 'token':
      //запись в локалсторадж
      //редирект на главную
      break
    case 'password':
      break
    case 'reset_password':
      break
    case 'verify_activation':
  }
  console.log(response, action)
}


