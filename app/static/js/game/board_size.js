const rotate = () => {
  if (!board_rotate) {
    board_rotate = "-"
  } else {
    board_rotate = ""
  }
  switch (board_position) {
    case 0:
      size0(0);
      break
    case 1:
      size1(0);
      break
    case 2:
      size2(0);
      break
    case 3:
      size3(0);
  }
}

const size0 = (time = 3) => {
  board_scale = 1.5
  board_size = 8
  board_position = 0
  let _style
  if (game.chess_variant !== 'iy-fib') {
    if (!board_rotate) {
      _style = "" +
        "div#board_path_top>div.coords.collum {" +
        "flex-flow: column-reverse;" +
        "transform: translate( 539px, -242px);" +
        "}" +
        "div#board_path_bottom>div.coords.collum {" +
        "flex-flow: column-reverse;" +
        "transform: translate( 539px, -2px);" +
        "}" +
        "div.coords.row {" +
        "transform: translate( 122px, 341px);" +
        "}" +
        "div.coord.a {" +
        "color: #86a666;" +
        "}"
    } else {
      _style = "" +
        "div#board_path_top>div.coords.collum {" +
        "flex-flow: column;" +
        "transform: translate( 122px, -238px) scale(-1);" +
        "}" +
        "div#board_path_bottom>div.coords.collum {" +
        "flex-flow: column;" +
        "transform: translate( 122px, 2px) scale(-1);" +
        "}" +
        "div.coords.row {" +
        "transform: translate( 118px, -41px) scale(-1);" +
        "flex-flow: row-reverse;" +
        "}" +
        "piece{" +
        "transform: scale(-1);" +
        "}" +
        "div.coord.b {" +
        "color: #86a666;" +
        "}"
    }
  } else {
    if (!board_rotate) {
      _style = "" +
        "div.coords.collum {" +
        "transition: " + time + "s;" +
        "flex-flow: column-reverse;" +
        "transform: translate( 539px, -2px);" +
        "}" +
        "div#board_path_top>div.coords.row {" +
        "display:none;" +
        "}" +
        "div#board_path_bottom>div.coords.row {" +
        "transform: translate( 2px, 341px);" +
        "}" +
        "div.coord.a {" +
        "color: #86a666;" +
        "}"
    } else {
      _style = "" +
        "div.coords.collum {" +
        "transition: " + time + "s;" +
        "flex-flow: column;" +
        "transform: translate( 122px, 2px) scale(-1);" +
        "}" +
        "div#board_path_top>div.coords.row {" +
        "transform: translate( -2px, -41px) scale(-1);" +
        "flex-flow: row-reverse;" +
        "}" +
        "piece{" +
        "transform: scale(-1);" +
        "}" +
        "div.coord.b {" +
        "color: #86a666;" +
        "}"
    }
  }
  if (board_style)
    board_style.innerHTML = "" +
      "#board{" +
      "transition: " + time + "s;" +
      "height: 480px; width: 480px;" +
      "transform: translate( 120px,  120px) scale(" + board_rotate + board_scale + ")" +
      "}" +
      "#board_path_top{" +
      "transition: " + time + "s;" +
      "transform: translate( -120px, 0px)" +
      "}" +
      "#board_path_bottom{" +
      "transition: " + time + "s;" +
      "transform: translate( -120px, -120px)" +
      "}" +
      ".size4{" +
      "opacity: 0;" +
      "}" + _style
  const bmask = ['f4', 'g4', 'f9', 'g9']
  bmask.forEach((value) => {
    hide_and_remove_piece(value, 8000)
  })
}

const size1 = (time) => {
  size0(time)
  board_position = 1
  if (board_style)
    board_style.innerHTML = board_style.innerHTML +
      ".size0{" +
      "opacity: 0;" +
      "}"
}

const size2 = (time) => {
  board_scale = 1.2
  board_size = 10
  board_position = 2
  let _style
  if (!board_rotate) {
    _style = "" +
      "div.coords.collum {" +
      "transition: " + time + "s;" +
      "flex-flow: column-reverse;" +
      "transform: translate( 659px, -1px);" +
      "}" +
      "div#board_path_top>div.coords.row {" +
      "display: none;" +
      "}" +
      "div#board_path_bottom>div.coords.row {" +
      "transform: translate( 2px, 341px);" +
      "}" +
      "div.coord.a {" +
      "color: #86a666;" +
      "}"
  } else {
    _style = "" +
      "div.coords.collum {" +
      "transition: " + time + "s;" +
      "flex-flow: column;" +
      "transform: translate( 123px, 1px) scale(-1);" +
      "}" +
      "div#board_path_top>div.coords.row {" +
      "transform: translate( -2px, -41px) scale(-1);" +
      "flex-flow: row-reverse;" +
      "}" +
      "div#board_path_bottom>div.coords.row {" +
      "display: none;" +
      "}" +
      "piece{" +
      "transform: scale(-1);" +
      "}" +
      "div.coord.b {" +
      "color: #86a666;" +
      "}"
  }
  if (board_style)
    board_style.innerHTML = "" +
      "#board{" +
      "transition: " + time + "s;" +
      "height: 600px; width: 600px;" +
      "transform: translate( 60px, 60px) scale(" + board_rotate + board_scale + ")" +
      "}" +
      "#board_path_top{" +
      "transition: " + time + "s;" +
      "transform: translate( -120px, 0px)" +
      "}" +
      "#board_path_bottom{" +
      "transition: " + time + "s;" +
      "transform: translate( -120px, -60px)" +
      "}" +
      ".size0, .size4{" +
      "opacity: 0;" +
      "}" + _style
}

const size3 = (time) => {
  board_scale = 1
  board_size = 12
  board_position = 3
  let _style
  if (!board_rotate) {
    _style = "" +
      "div.coords.collum {" +
      "transition: " + time + "s;" +
      "flex-flow: column-reverse;" +
      "transform: translate( 659px, -1px);" +
      "}" +
      "div#board_path_top>div.coords.row {" +
      "display: none;" +
      "}" +
      "div#board_path_bottom>div.coords.row {" +
      "transform: translate( 2px, 341px);" +
      "}" +
      "div.coord.a {" +
      "color: #86a666;" +
      "}"
  } else {
    _style = "" +
      "div.coords.collum {" +
      "transition: " + time + "s;" +
      "flex-flow: column;" +
      "transform: translate( 3px, 1px) scale(-1);" +
      "}" +
      "div#board_path_top>div.coords.row {" +
      "transform: translate( -2px, -41px) scale(-1);" +
      "flex-flow: row-reverse;" +
      "}" +
      "div#board_path_bottom>div.coords.row {" +
      "display: none;" +
      "}" +
      "piece{" +
      "transform: scale(-1);" +
      "}" +
      "div.coord.b {" +
      "color: #86a666;" +
      "}"
  }
  if (board_style)
    board_style.innerHTML = "" +
      "#board{" +
      "transition: " + time + "s;" +
      "height: 720px;width: 720px;" +
      "transform: scale(" + board_rotate + board_scale + ")" +
      "}" +
      "#board_path_top{" +
      "transition: " + time + "s;" +
      "transform: translate( 0px, 0px)" +
      "}" +
      "#board_path_bottom{" +
      "transition: " + time + "s;" +
      "transform: translate( 0px, 0px)" +
      "}" +
      ".size0{" +
      "opacity: 0;" +
      "}" + _style
  const bmask = ['b3', 'b10', 'c4', 'c9', 'd5', 'd8', 'i5', 'i8', 'j4', 'j9', 'k3', 'k10']
  bmask.forEach((value) => {
    hide_and_remove_piece(value, 8000)
  })
}

