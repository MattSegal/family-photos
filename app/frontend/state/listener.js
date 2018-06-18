// Listen for events that occur outside of React and dispatch actions to store
import actions from './actions'

const listener = (dispatch, getState) => {
  // Close toolbar on escape keypress
  document.onkeydown = e => {
    const isEscape = 'key' in e
      ? (e.key == 'Escape' || e.key == 'Esc')
      : e.keyCode == 27
    if (isEscape) {
      const state = getState()
      if (state.activeVenue) {
        dispatch(actions.clearVenue())
      }
      if (state.toolbarOpen) {
        dispatch(actions.closeToolbar())
      }
    }
  }
}

module.exports = listener
