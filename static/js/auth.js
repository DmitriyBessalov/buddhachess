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

formValidate = (event, path) => {
  event.preventDefault()
  const data = new FormData(event.target)
  const value = Object.fromEntries(data.entries())

  fetch(window.location.protocol + '//' + window.location.host + path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(value)
  }).then(
    async response => ({
      status: response.status,
      body: await response.text(),
    })
  ).then(
    response => {
      console.log(JSON.parse(response.body))
      for (const prop in value) {
        if (JSON.parse(response.body).detail[0].loc[1])
          if (JSON.parse(response.body).detail[0].loc[1] === prop) {
            let input = document.querySelector('[name=' + prop + ']')
            // input.classList.remove('is-valid')
            input.classList.add('is-invalid')
            let msg = document.querySelector('[name=' + prop + ']~.invalid-feedback')
            msg.innerHTML = JSON.parse(response.body).detail[0].msg
          } else {
            let input = document.querySelector('[name=' + prop + ']')
            // input.classList.add('is-valid')
            input.classList.remove('is-invalid')
            }
      }
    }
  )
  return true
}

const form = document.querySelector('.needs-validation')
form.addEventListener('submit', function (event) {
  if (formValidate(event, '/api/auth/register/'))
  AlertMDB("Вы успешно зарегистрировались! Теперь подтвердите ваш email, письмо отправленно", "green")
})


