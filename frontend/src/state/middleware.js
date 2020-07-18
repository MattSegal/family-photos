import api from './api'

// Upload images until they're all in the SUCESSS or FAIL state
const uploader = store => {
  const upload = store.getState().upload
  const pendingImages = upload.images.filter(image => image.state === 'NOT_SENT')
  if (pendingImages.length < 1) {
    store.dispatch({type: 'FINISH_UPLOAD'})
  } else {
    // Still images left to upload
    const pendingImage = pendingImages[0]
    store.dispatch({type: 'START_UPLOAD', imageName: pendingImage.name})
    api.image.upload(pendingImage)
    .then(() => {
      store.dispatch({type: 'SUCEESS_UPLOAD', imageName: pendingImage.name})
      store.dispatch({type: 'CONTINUE_UPLOAD', imageName: pendingImage.name})
    })
    .catch((error) => {
      console.error(error)
      store.dispatch({type: 'FAIL_UPLOAD', imageName: pendingImage.name})
      store.dispatch({type: 'CONTINUE_UPLOAD', imageName: pendingImage.name})
    })
  }
}

const uploadMiddleware = store => next => action => {
  if (action.type === 'REQUEST_UPLOAD' || action.type === 'CONTINUE_UPLOAD') {
    uploader(store)
  }
  return next(action)
}

module.exports = {
  uploadMiddleware,
}
