// Reducers
const reducers = {
  TOGGLE_TRAY: (state, action) => ({
    ...state,
    header: {
      ...state.header,
      trayOpen: !state.header.trayOpen,
    }
  }),
  PAGE_LOADED: (state, action) => ({
    ...state,
    // Really convoluted way to ensure unqiue values
    loadedPages: [...state.loadedPages, action.page].filter(
      (value, index, self) => self.indexOf(value) === index
    ),
  }),
  SET_TITLE: (state, action) => ({
    ...state,
    title: action.title,
  }),
  RECEIVE_ALBUM: (state, action) => ({
    ...state,
    albums: state.albums.map(album => album.id === action.data.id ? action.data : album),
  }),
  RECEIVE_ALBUMS: (state, action) => ({
    ...state,
    albums: action.data,
  }),
  SHOW_MODAL: (state, action) => ({
    ...state,
    modal: {
      isOpen: true,
      imageIdx: action.images ?
        action.images.map(i => i.id).indexOf(action.imageId) :
        null,
      images: action.images,
    }
  }),
  SCROLL_MODAL: (state, action) => {
    let imageIdx = state.modal.imageIdx
    const numImages = state.modal.images.length
    if (numImages < 1 || imageIdx + action.change < 0) {
      imageIdx = 0
    } else if (imageIdx + action.change > numImages - 1) {
      imageIdx = numImages - 1
    } else {
      imageIdx += action.change
    }
    return {
      ...state,
      modal: {
        ...state.modal,
        imageIdx: imageIdx,
      },
    }
  },
  CLOSE_MODAL: (state, action) => ({
    ...state,
    modal: {
      isOpen: false,
      imageIdx: 0,
      images: [],
    }
  }),
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
