dnaForm.onsubmit = async (e) => {
  e.preventDefault()
  const
    data = new FormData(e.target),
    value = Object.fromEntries(data.entries())
  let
    response,
    form_valid = true

  console.log(JSON.stringify(value))

  response = await fetch(e.path[0].action, {
    method: e.path[0].attributes.method.nodeValue,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(value)
  })

  console.log(await response)
  const result = await response.json()

  for (const prop in value) {
    let input = document.querySelector('[name=' + prop + ']')
    if (result?.detail?.[0]?.loc?.[1] === prop) {
      input.classList.remove('is-valid')
      input.classList.add('is-invalid')
      let msg = document.querySelector('[name=' + prop + ']~.invalid-feedback')
      msg.innerHTML = result.detail[0].msg
      form_valid = false
    } else {
      input.classList.add('is-valid')
      input.classList.remove('is-invalid')
    }
  }
}