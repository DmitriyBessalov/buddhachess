const color_block = () => {
  if (Boolean(move % 2) !== color) {
    document.querySelector(`#board_rotate`).style.pointerEvents = "none"
  } else {
    document.querySelector(`#board_rotate`).style.pointerEvents = "unset"
  }
  color_current_move = Boolean(move % 2)
}

let movesArray = new Array()

const mov = (r, t) => {
  const regex = /([a-l])(10|11|12|[1-9])([a-l])(10|11|12|[1-9])/g
  let arr = regex.exec(r)
  const s = coordinate_shift_from_view(arr[1], arr[2])
  const e = coordinate_shift_from_view(arr[3], arr[4])
  set_piece_position(arr[1] + arr[2], s.shift_x, s.shift_y, e.shift_x, e.shift_y, arr[3] + arr[4], t)
  movesArray.push([arr[1], arr[2], arr[3], arr[4]])
  next_move(move)
  color_block()
  board_click = false
}

const chess_move = (piece, _mouse_position_dragend, _mouse_position_dragstart) => {
  const cName = piece.querySelector(`piece`).className.split(' ')
  console.log(cName[0], cName[1], _mouse_position_dragstart.view + '-' + _mouse_position_dragend.view)
  if ((((cName[0] === "white") && (color === true)) ||
      ((cName[0] === "black") && (color === false))) &&
    (_mouse_position_dragstart.view !== _mouse_position_dragend.view)) {

    window.websocket.send('{' +
      '"cmd":"move",' +
      '"move_num":"' + movesArray.length + '",' +
      '"move":"' + piece.id.substr(6) + _mouse_position_dragend.view + '"' +
      '}')
    move++
    mov(_mouse_position_dragstart.view + _mouse_position_dragend.view, 0)
  }
}

const dragstart=(evt)=>{
  board_position_top = board.getBoundingClientRect().top
  mouse_position_dragstart = coordinate_shift(mouse_position(evt))
  select_piece = document.querySelector("#block_" + mouse_position_dragstart.view)
}

board.addEventListener(`dragstart`, (evt) => {
  dragstart(evt)
})

board.addEventListener(`dragover`, (evt) => {
  mouse_position_dragover = mouse_position(evt)
  if (mouse_position_old_dragover.x !== mouse_position_dragover.x || mouse_position_old_dragover.y !== mouse_position_dragover.y) {
    mouse_position_old_dragover = mouse_position_dragover
    // console.log('mouseover', mouse_position_dragover)
  }
  // console.log('mousemove', evt.layerX, evt.layerY,)
})

const dragend=(evt)=>{
  const check = mouse_position(evt)
  console.log(check.view, mouse_position_dragstart.view)
  if ((check.x >= 0) && (check.y >= 0) && (check.x < board_size) && (check.y < board_size)) {
    mouse_position_dragend = coordinate_shift(mouse_position(evt))
    console.log(mouse_position_dragend.view, mouse_position_dragstart.view)
    if (select_piece)
      chess_move(select_piece, mouse_position_dragend, mouse_position_dragstart)
  }
  evt.target.classList.remove(`dragover`)
}

board.addEventListener(`dragend`, (evt) => {
  dragend(evt)
})


const fibonacci = (move) => {
  const fib = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765,]
  if (move % 2) {
    move = move / 2 + 1.5
    let f = 0
    while (fib[f] <= move) {
      f++
    }
    switch (f % 6) {
      case 1:
        if (board_position !== 0) size0(1);
        break
      case 2:
      case 0:
        if (board_position !== 1) size1(1);
        break
      case 3:
      case 5:
        if (board_position !== 2) size2(1);
        break
      case 4:
        if (board_position !== 3) size3(1)
    }
  }
}

const moves_list = document.querySelector(`#moves_list`)
const next_move = (_move) => {
  if (game.chess_variant === 'iy-fib')
    fibonacci(_move)
  if (movesArray[_move]) {
    let div2 = document.createElement('div')
    div2.innerHTML = movesArray[_move][0] + movesArray[_move][1] + '-' + movesArray[_move][2] + movesArray[_move][3]
    if (_move % 2) {
      const div = document.querySelector(`#moves_list > div:last-child`)
      div.appendChild(div2)
    } else {
      let div = document.createElement('div')
      let div3 = document.createElement('div')
      div3.innerHTML = (_move / 2 + 1) + '. '
      div.appendChild(div3)
      div.appendChild(div2)
      moves_list.appendChild(div)
      moves_list.parentNode.scrollTop = moves_list.parentNode.scrollHeight
    }
  }
}

const coordinate_shift_from_view = (x, y) => {
  let position = {}
  position['x'] = x.charCodeAt(0) - 99

  if (game.chess_variant === 'iy-fib') {
    if (board_size === 12)
      position.x = x.charCodeAt(0) - 97
    position['y'] = 12 - y
    position = coordinate_shift(position, true)
  } else {
    position['y'] = 8 - y
    position.x = x.charCodeAt(0) - 97
    position = coordinate_shift(position)
  }
  return (position)
}