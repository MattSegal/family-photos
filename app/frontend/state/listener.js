// Listen for events that occur outside of React and dispatch actions to store
import actions from './actions'

const listener = (dispatch, getState) => {
  // Handle key press
  document.onkeydown = e => {
    const isEscape = 'key' in e ? (e.key == 'Escape' || e.key == 'Esc') : e.keyCode == 27
    const isLeft = 'key' in e ? e.key == 'ArrowLeft' : e.keyCode == 37
    const isRight = 'key' in e ? e.key == 'ArrowRight' : e.keyCode == 39
    if (isEscape) {
      dispatch(actions.pressEsc())
    } else if (isRight) {
      dispatch(actions.pressRight())
    } else if (isLeft) {
      dispatch(actions.pressLeft())
    }
  }

  // Handle left / right swipe - thanks Stack Overflow!
  let xDown = null
  let yDown = null

  document.ontouchstart = e => {
      xDown = e.touches[0].clientX
      yDown = e.touches[0].clientY
  }
  document.ontouchmove = e => {
      if ( ! xDown || ! yDown ) return
      const xUp = e.touches[0].clientX
      const yUp = e.touches[0].clientY

      const xDiff = xDown - xUp
      const yDiff = yDown - yUp

      if ( 3 * Math.abs( xDiff ) > Math.abs( yDiff ) ) {
          if ( xDiff > 0 ) {
              /* left swipe - same as right key press */
              dispatch(actions.pressRight())
          } else {
              /* right swipe - same as left key press */
              dispatch(actions.pressLeft())
          }
      } else {
          if ( yDiff > 0 ) {
              /* up swipe */
          } else {
              /* down swipe */
          }
      }
      /* reset values */
      xDown = null
      yDown = null
  }
}

module.exports = listener

