const page_session = Math.round(Math.random() * 10 ** 12)
let ws_init = false

const chess_variant = {
  "iy": "Инь-ян",
  "flang": "Фланговая",
  "iy-flang": "Инь-ян / Фланговая",
  "iy-fib": "Инь-ян / Фибоначчи",
  "classic": "Класические",
  "960": "Фишера 960",
}

const color = {
  true: "Белыми",
  false: "Черными",
}

RemoveElem = (id) => {
  document.getElementById(id)?.remove()
  if (!my_games_list.childNodes.length)
    my_games.style.display = "none"
}

wsReady = () => {
  if (window.websocket === undefined || window.websocket?.readyState === 3) {
    window.websocket = new WebSocket('ws://localhost:8000/ws/game/create/' + page_session + '/' + access_token)
  }

  if (window.websocket?.readyState === 0) {
    setTimeout(wsReady, 1000)
    return
  }

  if (!ws_init) {
    ws_init = true
    window.websocket.send('{"cmd": "show_games"}')

    window.websocket.onclose = () => {
      console.log('onclose')
      delete window.websocket
      ws_init = false
      setTimeout(wsReady, 3000)
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

      let listGames = ''
      let MylistGames = ''


      if (message.cmd === "list_games") {
        for (key in message.list_games) {
          // console.log(message.list_games[key].user, sessionStorage.getItem('username'))
          if (message.list_games[key].user === sessionStorage.getItem('username')) {
            MylistGames += '<div class="border rounded-2 p-3 mt-3 text-start" id="game_id_' + message.list_games[key].game_id + '">\
              <div class="d-flex justify-content-between">\
                <p>\
                  ' + chess_variant[message.list_games[key].chess_variant] + '<br\>\
                  ' + color[message.list_games[key].color] + '\
                </p>\
                <div>\
                  Ожидание соперника \
                  <div class="spinner-border spinner-border-sm" role="status">\
                    <span class="visually-hidden">Loading...</span>\
                  </div>\
                </div>\
              </div>\
            </div>'
          } else {
            listGames += '<div class = "border rounded-2 p-3 mt-3 text-start" id="game_id_' + message.list_games[key].game_id + '">\
                <div class = "d-flex justify-content-between">\
                  <p>\
                    ' + chess_variant[message.list_games[key].chess_variant] + '<br\>\
                    ' + color[!message.list_games[key].color] + '\
                  </p>\
                  <div class="chip chip-md">\
                    <img src="https://secure.gravatar.com/avatar/4b3d3362efa67b11badb99f87beefa95?s=48&d=mm&r=g" alt="Contact Person"/>\
                    ' + message.list_games[key].user + '\
                  </div>\
                </div>\
                <button class="btn btn-primary btn-block mt-3" id="' + message.list_games[key].game_id + '" onclick="joingame(this)">\
                  Играть\
                </button>\
              </div>'
          }
          setTimeout(RemoveElem, message.list_games[key].ttl * 1000 - 3000, 'game_id_' + message.list_games[key].game_id)
        }

        if (MylistGames === "")
          my_games.style.display = "none"
        else
          my_games.style.display = "block"
        my_games_list.innerHTML = MylistGames
        list_games.innerHTML = listGames

        CreateGame.onsubmit = async (e) => {
          e.preventDefault()
          const data = new FormData(event.target)
          const formJSON = Object.fromEntries(data.entries())
          formJSON['cmd'] = "create_game"
          window?.websocket.send(JSON.stringify(formJSON))
        }

        joingame=(event)=>{
          // console.log(event.id)
          window?.websocket.send('{"cmd":"join_game","game_id": "' + event.id + '"}')
        }
      }
    }
  }
}

auth_session().then(
  r => {
    wsReady()
  }
)

