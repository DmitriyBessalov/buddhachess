const create_piece = (code_piece, id, _x, _y) => {
  //console.log( code_piece, id, _x, _y)
  let div = document.createElement('div')
  div.classList = 'piece_rotate'
  let piece = document.createElement('piece')
  piece.setAttribute("class", code_piece)
  if (code_piece === code_piece.toUpperCase()) {
    piece.setAttribute("class", "white " + code_piece)
  } else {
    piece.setAttribute("class", "black " + code_piece)
  }
  piece.id = 'start_' + id
  div.appendChild(piece)
  div.draggable = true
  set_piece_position(div, undefined, undefined, _x, _y, id)
}

const remove_piece = (old_piece) => {
  old_piece.remove()
}

const hide_and_remove_piece = (id, time_animation= 400) => {
  let old_piece = document.querySelector("#block_" + id)
  if (old_piece) {
    old_piece.style.transition = 'opacity ' + time_animation + 'ms linear'
    old_piece.style.opacity = '0'
    setTimeout(remove_piece, 10000, old_piece)
  }
}

const set_piece_position = (piece, end_x, end_y, _x, _y, id, time_animation = 0,) => {
  //console.log(piece, end_x, end_y, _x, _y, id)
  hide_and_remove_piece(id)
  if (typeof (piece) === "string")
    piece = document.querySelector("#block_" + piece)

  piece.id = "block_" + id
  if (position_board_path(_y) === "top") {
    piece.setAttribute("style", "transform: translate(" + _x * 60 + "px, " + _y * 60 + "px);")
    if (board_path_top)
      board_path_top.appendChild(piece)
  } else {
    piece.setAttribute("style", "transform: translate(" + _x * 60 + "px, " + (_y - 6) * 60 + "px);")
    if (board_path_bottom)
      board_path_bottom.appendChild(piece)
  }
}