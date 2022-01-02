let game = {}
game['game_id'] = document.location.pathname.split('/')[3]

let
  board,
  board_path_top,
  board_path_bottom,
  board_style,
  board_scale,
  board_size,
  board_position,
  FEN,
  color,
  color_current_move = true,
  mouse_position_dragstart = {},
  mouse_position_dragover = {},
  mouse_position_old_dragover = {},
  mouse_position_dragend = {},
  board_position_top,
  board_rotate = "",
  board_click = false,
  move = -1,
  moves,
  game_init_status = false,
  select_piece

board = document.querySelector(`#board`)
board_path_top = document.querySelector(`#board_path_top`)
board_path_bottom = document.querySelector(`#board_path_bottom`)
board_style = document.querySelector(`#board_style`)


wsReady = () => {
  if (window.websocket === undefined || window.websocket?.readyState === 3) {
    let s = ''
    if (location.protocol === 'https:') {
      s = 's'
    }
    window.websocket = new WebSocket('ws' + s + '://' + location.host + '/ws/game/' + game.game_id + '/' + access_token)
  }

  if (window.websocket?.readyState === 0) {
    setTimeout(wsReady, 1000)
    return
  }

  if (!ws_init) {
    ws_init = true
    window.websocket.send('{"cmd": "join_game"}')

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
        case "join_game": {
          game = message

          if (game.user_white === localStorage.getItem("username")) {
            color = true
          } else if (game.user_black === localStorage.getItem("username")) {
            color = false
          }

          FEN = game.FEN

          game_init()
          break
        }
        case "move": {
          move = parseInt(message.move_num)
          color_block()
          if (color_current_move === color) {
            mov(message.move, 1.5)
          }
        }
      }
    }
  }
}

const generate_start_position = () => {
  if (FEN) {
    let line = FEN.split(" ")[0].split("/")
    line.forEach((value, key) => {
      let position = {}
      position['x'] = 0
      let i = 0
      for (; position.x < 12; i++) {
        if (value[i] && (Number.isNaN(parseInt(value[i], 10)))) {
          position['y'] = key
          position = coordinate_shift(position)
          create_piece(value[i], position.view, position.shift_x, position.shift_y)
          position.x++
        } else {
          position.x = position.x + Number(value[i])
        }
      }
    })
  }
}

game_init = () => {
  if (!game_init_status) {
    game_init_status = true
    if (game.chess_variant === 'iy-fib') {
      size3(0)
      if (color === false)
        rotate()
      generate_start_position()
      setTimeout(size0, 3000)
    } else {
      if (game.chess_variant === 'iy' || game.chess_variant === 'classic')
        size1(0)
      else
        size0(0)
      if (color === false)
        rotate()
      generate_start_position()
    }
//get_start_moves(moves)
    color_block()
  }
}

if (document.documentElement.clientWidth < document.documentElement.clientHeight){
    html.classList.add('horizon')
    board_pozition.style.transform='scale(' + document.documentElement.clientWidth/740 + ')'
}

auth_session().then(
  r => {
    wsReady()
  }
)