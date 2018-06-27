import api from './api'

module.exports = {
  // Redux's store.dispatch is aliased to 'd' for brevity
  toggleTray: () => ({type: 'TOGGLE_TRAY'}),
  pageLoaded: page => ({type: 'PAGE_LOADED', page: page}),
  fetchAlbum: id => d => {
    d({type: 'REQUEST_API'})
    return api.album.get(id)
      .then( r => r.data)
      .then( data => d({type: 'RECEIVE_ALBUM', data: data}))
      .catch((error) => {
        console.error(error)
        d({type: 'API_ERROR'})
      })
  },
  listAlbums: () => d => {
    d({type: 'REQUEST_API'})
    return api.album.list()
      .then( r => r.data)
      .then( data => d({type: 'RECEIVE_ALBUMS', data: data}))
      .catch((error) => {
        console.error(error)
        d({type: 'API_ERROR'})
      })
  },
  setTitle: title => ({type: 'SET_TITLE', title: title}),
  showModal: (imageId, images) => ({type: 'SHOW_MODAL', imageId: imageId, images: images}),
  closeModal: () => ({type: 'CLOSE_MODAL'}),
  scrollModal: change => ({type: 'SCROLL_MODAL', change: change}),
  pressLeft: () => (d, getState) => {
    const state = getState()
    if (state.modal.isOpen) {
      d({type: 'SCROLL_MODAL', change: -1})
    }
  },
  pressRight: () => (d, getState) => {
    const state = getState()
    if (state.modal.isOpen) {
      d({type: 'SCROLL_MODAL', change: 1})
    }
  },
  pressEsc: () => (d, getState) => {
    const state = getState()
    if (state.modal.isOpen) {
      d({type: 'CLOSE_MODAL'})
    }
  },
}
