// Reducers
const reducers = {
  // Open / close header menu tray
  TOGGLE_TRAY: (state, action) => ({
    ...state,
    header: {
      ...state.header,
      trayOpen: !state.header.trayOpen,
    }
  }),

  // A page has has its images loaded
  PAGE_LOADED: (state, action) => ({
    ...state,
    loadedPages: [...state.loadedPages, action.page].filter(isUnique),
  }),

  // Set page title
  SET_TITLE: (state, action) => ({
    ...state,
    title: action.title,
  }),

  // Album data fetched from the backend API
  RECEIVE_ALBUM: (state, action) => ({
    ...state,
    albums: state.albums.map(album => album.id === action.data.id ? action.data : album),
  }),
  RECEIVE_ALBUMS: (state, action) => ({
    ...state,
    albums: action.data,
  }),

  // Image view modal
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

  // Image uploads
  SELECT_UPLOAD_ALBUM: (state, action) => {
      const newUpload = {
      ...state.upload,
      album: state.albums.find(a => a.id == action.album) || '',
    }
    newUpload.images = state.upload.images.map(i => ({...i, album: newUpload.album}))
    newUpload.uploadValid = isUploadValid(newUpload)
    return { ...state, upload: newUpload }
  },
  ADD_UPLOAD_IMAGES: (state, action) => {
    const images = []
    for (let i = 0; i < action.files.length; i++) {
      const image = action.files[i]
      if (isValidImage(image) && !imageAlreadyExists(image, state.upload.images, images)) {
        images.push({
          album: state.upload.album,
          name: image.name,
          file: image,
          src: URL.createObjectURL(image),
          state: UPLOAD_STATE.NOT_SENT,
        })
      }
    }
    const newUpload = {
      ...state.upload,
      images: [...state.upload.images, ...images],
    }
    newUpload.uploadValid = isUploadValid(newUpload)
    return { ...state, upload: newUpload }
  },
  CLEAR_IMAGES: (state, action) => ({ ...state, upload: { ...state.upload, images: [] } }),
  REQUEST_UPLOAD: (state, action) => ({
    ...state,
    upload: {
      ...state.upload,
      uploading: true,
    },
  }),
  START_UPLOAD: (state, action) => setImageUploadState(action.imageName, UPLOAD_STATE.UPLOADING, state),
  SUCEESS_UPLOAD: (state, action) => setImageUploadState(action.imageName, UPLOAD_STATE.SUCCESS, state),
  FAIL_UPLOAD: (state, action) => setImageUploadState(action.imageName, UPLOAD_STATE.FAIL, state),
  FINISH_UPLOAD: (state, action) => ({
    ...state,
    upload: {
      ...state.upload,
      uploadValid: false,
      uploading: false,
    },
  }),
}

const UPLOAD_STATE = {
  SUCCESS: 'SUCCESS',
  FAIL: 'FAIL',
  UPLOADING: 'UPLOADING',
  NOT_SENT: 'NOT_SENT',
}

const setImageUploadState = (imageName, imageState, state) => ({
  ...state,
  upload: {
    ...state.upload,
    images: state.upload.images.map(i => {
      if (i.name === imageName) {
        return { ...i, state: imageState}
      }
      return i
    })
  },
})

const isUploadValid = upload => upload.images.length > 0 && Boolean(upload.album.id)

const isValidImage = f =>
  f.type.match('^image/jpeg') &&
  f.size > 0

const imageAlreadyExists = (image, oldImages, newImages) =>
  oldImages.map(i => i.name).includes(image.name) ||
  newImages.map(i => i.name).includes(image.name)

const isUnique = (value, index, self) => self.indexOf(value) === index

module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
