const mouse_position = (evt) => {
  let mouse_pos = {}
    mouse_pos['x'] = (Math.ceil(evt.layerX / (60 * board_scale))) - 1
    mouse_pos['y'] = Math.ceil((evt.y - board_position_top) / (60 * board_scale)) - 1

  if (board_rotate) {
    mouse_pos.x = board_size - mouse_pos['x'] - 1
    mouse_pos.y = board_size - mouse_pos['y'] - 1
  }
  // console.log(mouse_pos)
  return mouse_pos
}

const position_board_path = (mouse_pos_y) => {
  if (board_size / 2 <= mouse_pos_y) {
    return 'bottom'
  } else {
    return 'top'
  }
}


const coordinate_shift = (position, shift = false) => {
  position['shift_x'] = position.x
  position['shift_y'] = position.y

  if (game.chess_variant !== 'iy-fib') {
    position['shift_x'] = position.x + 2
    if ((position_board_path(position.y) === 'bottom') && (!shift)) {
      position['shift_y'] = position.y + 4
      position['view'] = String.fromCharCode(95 + position.shift_x) + (12 - position.shift_y)
    } else {
      position['shift_y'] = position.y
      position['view'] = String.fromCharCode(95 + position.shift_x) + (8 - position.shift_y)
    }
  } else {
    if (board_size !== 12) {
      position['shift_x'] = position.x + 2
      if ((position_board_path(position.y) === 'bottom') && (!shift)) {
        if (board_size === 8) {
          position['shift_y'] = position.y + 4
        } else {
          position['shift_y'] = position.y + 2
        }
      }
    }
    position['view'] = String.fromCharCode(97 + position.shift_x) + (12 - position.shift_y)
  }
  //console.log(position)
  return position
}