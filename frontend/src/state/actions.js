import api from './api'

// Redux's store.dispatch is aliased to 'd' for brevity
module.exports = {
  // Open / close header menu tray
  toggleTray: () => ({type: 'TOGGLE_TRAY'}),

  // A page has had its images loaded
  pageLoaded: page => ({type: 'PAGE_LOADED', page: page}),

  // Fetch an album from the backend
  fetchAlbum: id => d => {
    d({type: 'REQUEST_API'})
    return api.album.get(id)
      .then( data => d({type: 'RECEIVE_ALBUM', data: data}))
      .catch((error) => {
        console.error(error)
        d({type: 'API_ERROR'})
      })
  },

  // Fetch a list of albums from the backend
  listAlbums: () => d => {
    d({type: 'REQUEST_API'})
    return api.album.list()
      .then( data => d({type: 'RECEIVE_ALBUMS', data: data}))
      .catch((error) => {
        console.error(error)
        d({type: 'API_ERROR'})
      })
  },

  // Set page title
  setTitle: title => ({type: 'SET_TITLE', title: title}),

  // Image modal
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

  // Image uploads
  selectAlbum: album => ({ type: 'SELECT_UPLOAD_ALBUM', album: album }),
  addImages: files => ({ type: 'ADD_UPLOAD_IMAGES', files: files }),
  clearImages: () => d => {
    const confirmed = window.confirm('Are you sure you want to clear chosen images?')
    if (confirmed) {
      d({type: 'CLEAR_IMAGES'})
    }
  },
  uploadImages: () => d => {
    d({type: 'REQUEST_UPLOAD'})
  },
}
