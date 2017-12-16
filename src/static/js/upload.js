// TODO: Check if file is already uploaded via API
// todo - progress bar and/or upload speed

// TODO - upload tags
// #select-album
// List of current album names
// Ability to add new album
// select album - must be done before upload
// all files uploaded are tagged to album

// home page
// show top 12 photos from every album thumb only
// link to album
// album page (current index page)

// TODO - do this with regex

SIGN_URL = window.location.pathname.includes('/dev/')
  ? '/dev/api/sign'
  : '/api/sign'


// Uploader states
STATES = {
  SELECT: 0,
  SIGNATURE: 1,
  UPLOADING: 2,
  UPLOADED: 3,
}

const fileInput = document.getElementById('file-input')

fileInput.onchange = () => {
    const files = fileInput.files
    const uploader = new ImageUploader(files)
}


class ImageUploader {

  constructor(files) {
    // Cache DOM
    this.statusEl = document.getElementById('status')
    this.uploadListEl = document.getElementById('upload-list')

    this.imageUploads = []
    this.signedImageCount = 0
    this.uploadingImageCount = 0
    this.uploadedImageCount = 0
    this.failedImageCount = 0

    // Ensure files selected
    this.setState(STATES.SELECT)
    if (!files.length > 0) return
    this.setState(STATES.SIGNATURE)

    for (let idx = 0; idx < files.length; idx++) {
      this.imageUploads.push(new ImageUpload(files[idx], this.uploadListEl))
    }

    // Request S3 signatures for each image
    this.imageUploads.forEach(i => i.getSignature(this.onSignatureFetched.bind(this)))
  }

  onSignatureFetched() {
    this.signedImageCount += 1
    if (this.signedImageCount === this.imageUploads.length) {
      this.downloadImages(2)
      this.setState(STATES.UPLOADING)
    }
  }

  downloadImages(count) {
    if (this.imageUploads.length < 1) {
      return
    }
    for (let i = 0; i < count; i++) {
      const img = this.imageUploads.pop()
      if (!img) continue
      img.upload(this.onUploadFinished.bind(this), this.onUploadFailed.bind(this))
      this.uploadingImageCount += 1
    }
  }

  onUploadFinished() {
    this.uploadedImageCount += 1
    this.uploadingImageCount -= 1
    this.checkFinished()
  }

  onUploadFailed() {
    this.failedImageCount += 1
    this.uploadingImageCount -= 1
    this.checkFinished()
  }

  checkFinished() {
    this.downloadImages(1)
    this.updateStatus('Uploading images...', true)
    const numFinished = this.uploadedImageCount + this.failedImageCount
    if (numFinished === this.imageUploads.length) {
      this.setState(STATES.UPLOADED)
    }
  }

  setState(state) {
    this.state = state
    switch(state) {
        case STATES.SIGNATURE:
            this.updateStatus('Preparing images for upload...', true)
            break
        case STATES.UPLOADING:
            this.updateStatus('Uploading images...', true)
            break
        case STATES.UPLOADED:
            this.updateStatus('Upload finished', true)

            break
        case STATES.SELECT:
        default:
          this.updateStatus('Select image(s) to upload', false)
          for (let idx = 0; idx < this.uploadListEl.children.length; idx++) {
            this.uploadListEl.removeChild(this.uploadListEl.children[idx])
          }
    }
  }

  updateStatus(msg, showCounts) {
    this.statusEl.innerHTML = '<p><strong>'+msg+'</strong></p>'
    if (showCounts) {
      this.statusEl.innerHTML += '<p>Pending: '+this.imageUploads.length+'</p>'
      this.statusEl.innerHTML += '<p>Uploading: '+this.uploadingImageCount+'</p>'
      this.statusEl.innerHTML += '<p>Uploaded: '+this.uploadedImageCount+'</p>'
      this.statusEl.innerHTML += '<p>Failed: '+this.failedImageCount+'</p>'
    }
  }
}


class ImageUpload {
  constructor(file, uploadListEl) {
    this.file = file
    // TODO: check file.size in bytes
    this.s3Url = false
    this.s3SignatureData = false

    this.divEl = document.createElement("div")
    this.divEl.classList.add('upload-image')
    this.paraEl = document.createElement("p")
    this.pendingMessage('Requesting upload...')

    this.imageEl = new Image()
    this.imageEl.height = 140
    this.imageEl.onload = () => uploadListEl.appendChild(this.divEl)

    this.divEl.appendChild(this.imageEl)
    this.divEl.appendChild(this.paraEl)

    this.imageEl.src =  URL.createObjectURL(this.file)
}

  getSignature(callback) {
    const xhr = new XMLHttpRequest()
    const onFail = () => {
      console.warn('Signature request failure for ', this.file.name, xhr.status, xhr.responseText)
      this.failMessage('Upload not approved')
      callback()
    }
    const onSuccess = () => {
      if (xhr.status !== 200) {
        onFail()
        return
      }
      console.warn('Signature request success for', this.file.name)
      const response = JSON.parse(xhr.responseText)
      this.s3Url = response.url
      this.s3SignatureData = response.data
      this.pendingMessage('Upload approved, waiting...')
      callback()
    }

    const qs = {
      file_name: this.file.name,
      file_type: this.file.type
    }
    const url = SIGN_URL + '?' + buildQuerystring(qs)
    xhr.open('GET', url)
    xhr.onload = onSuccess
    xhr.onerror = onFail
    console.warn('Requesting S3 upload signature for', this.file.name)
    xhr.send()
  }

  upload(successCallback, failCallBack) {
    this.paraEl.style.color = 'orange'
    this.divEl.style.order = '-1'
    this.paraEl.innerText = 'Uploading image...'
    const xhr = new XMLHttpRequest()
    const onFail = () => {
      console.warn('File upload failure for ', this.file.name, xhr.status, xhr.responseText)
      this.failMessage('Upload failed :(')
      failCallBack()
    }
    const onSuccess = () => {
      if (xhr.status !== 200 && xhr.status !== 204) {
        onFail()
        return
      }
      console.warn('File upload success for ', this.file.name, xhr.status, xhr.responseText)
      this.successMessage('Upload success :)')
      successCallback()
    }

    // Build and send form
    xhr.open("POST", this.s3Url)
    const postData = new FormData()
    for (let key in this.s3SignatureData.fields) {
      postData.append(key, this.s3SignatureData.fields[key]);
    }
    postData.append('file', this.file);
    xhr.onload = onSuccess
    xhr.onerror = onFail
    console.warn('Uploading', this.file.name)
    xhr.send(postData)
  }

  pendingMessage(msg) {
      this.paraEl.innerText = msg
      this.paraEl.style.color = 'orange'
      this.divEl.style.order = '-1'
  }

  successMessage(msg) {
      this.paraEl.innerText = msg
      this.paraEl.style.color = 'green'
      this.divEl.style.order = '0'
  }

  failMessage(msg) {
      this.paraEl.innerText = msg
      this.paraEl.style.color = 'red'
      this.divEl.style.order = '1'
  }
}

const buildQuerystring = qs => Object.keys(qs)
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(qs[key]))
    .join('&')
