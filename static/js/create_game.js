const page_session = Math.random()
let access_token,
  ws_init = false

console.log(page_session)

wsReady = () => {
  if (window.websocket === null || window.websocket.readyState === 4) {
    window.websocket = new WebSocket('ws://localhost:8000/ws/game/' + page_session + '/' + access_token + '/')
  }

  if (window.websocket.readyState === 0) {
    setTimeout(wsReady, 100)
    return
  }

  if (!ws_init) {
    ws_init = true
    let values = {}
    values['cmd'] = "show_games"
    values['access_token'] = "null"

    console.log(JSON.stringify(values))
    window.websocket.send(JSON.stringify(values))
    window.websocket.onclose = () => {
      console.log('onclose')
      setTimeout(wsReady, 100)
    }

    window.websocket.onmessage = function (e) {
      let message = JSON.parse(e.data)
      console.log(message)

      switch (message.cmd) {
        case "anonimous_login": {
          sessionStorage.setItem("access_token", message.access_token)
          break
        }
        case "join_game": {
          if (message.rival_black === localStorage.getItem("username") ||
            message.rival_white === localStorage.getItem("username")
          ) {
            sessionStorage.setItem("game_id_" + message.game_id, JSON.stringify(message))
            location.replace('/ru/game/' + message.game_id)
          }
        }
      }

      if (((message.cmd === "list_games") || (message.cmd === "join_game"))) {
        // setGameList(message.list_games)
        // Object.entries(message.list_games).forEach(([key, value]) => {
        //   setTimeout(rmGame, (value.ttl - 1) * 1000, value.game_id)
        // })
      }
    }

    CreateGame.onsubmit = async (e) => {
      e.preventDefault()
      const data = new FormData(event.target)
      const formJSON = Object.fromEntries(data.entries())
      window.websocket.send(JSON.stringify(formJSON))
    }


  }
}

auth_session().then(
  r => {
    access_token = r
    wsReady()
  }
)

