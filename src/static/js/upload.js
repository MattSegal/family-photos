// TODO: Check if file is already uploaded via API

SIGN_URL = '/api/sign'
UPLOAD_URL = '/api/upload'

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
    this.uploadedImageCount = 0
    
    // Ensure files selected
    this.setState(STATES.SELECT)
    if (!files.length > 0) return
    this.setState(STATES.SIGNATURE)

    for (let idx = 0; idx < files.length; idx++) {
      this.imageUploads.push(new ImageUpload(files[idx], this.uploadListEl))
    }

    // Request S3 signatures for each image  
    // this.imageUploads.forEach(i => i.getSignature(this.onSignatureFetched.bind(this)))
    this.imageUploads.forEach(i => i.upload(this.onUploadFinished.bind(this)))
  }

  onSignatureFetched() {
    this.signedImageCount += 1
    if (this.signedImageCount === this.imageUploads.length) {
      this.setState(STATES.UPLOADING)
      this.imageUploads.forEach(i => i.upload(this.onUploadFinished.bind(this)))
    }
  }

  onUploadFinished() {
    this.uploadedImageCount += 1
    if (this.uploadedImageCount === this.imageUploads.length) {
      this.setState(STATES.UPLOADED)
    }
  }

  setState(state) {
    this.state = state
    switch(state) {
        // case STATES.SIGNATURE:
        //     this.statusEl.innerText = 'Preparing images for upload...'
        //     break
        case STATES.UPLOADING:
            this.statusEl.innerText = 'Uploading images...'
            break
        case STATES.UPLOADED:
            this.statusEl.innerText = 'Upload finished'
            break
        case STATES.SELECT:
        default:
          this.statusEl.innerText = 'Select image(s) to upload'
          for (let idx = 0; idx < this.uploadListEl.children.length; idx++) {
            this.uploadListEl.removeChild(this.uploadListEl.children[idx])
          }
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
    this.paraEl.style.color = 'orange'
    this.paraEl.innerText = 'Requesting upload...'

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
      this.paraEl.style.color = 'red'
      this.paraEl.innerText = 'Upload not approved'
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
      this.paraEl.style.color = 'green'
      this.paraEl.innerText = 'Upload approved'
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

  upload(callback) {
    this.paraEl.style.color = 'orange'
    this.paraEl.innerText = 'Uploading image...'
    const xhr = new XMLHttpRequest()
    const onFail = () => {
      console.warn('File upload failure for ', this.file.name, xhr.status, xhr.responseText)
      this.paraEl.style.color = 'red'
      this.paraEl.innerText = 'Upload failed :('
      callback()
    }
    const onSuccess = () => {
      if (xhr.status !== 200 && xhr.status !== 204) {
        onFail()
        return
      }
      console.warn('File upload success for ', this.file.name, xhr.status, xhr.responseText)
      this.paraEl.style.color = 'green'
      this.paraEl.innerText = 'Upload success :)'
      callback()
    }

    // Build and send form
    xhr.open("POST", UPLOAD_URL)
    const postData = new FormData()
    postData.append('file', this.file);
    xhr.onload = onSuccess
    xhr.onerror = onFail
    console.warn('Uploading', this.file.name)
    xhr.send(postData)
  }

  s3Upload(callback) {
    this.paraEl.style.color = 'orange'
    this.paraEl.innerText = 'Uploading image...'
    const xhr = new XMLHttpRequest()
    const onFail = () => {
      console.warn('File upload failure for ', this.file.name, xhr.status, xhr.responseText)
      this.paraEl.style.color = 'red'
      this.paraEl.innerText = 'Upload failed :('
      callback()
    }
    const onSuccess = () => {
      if (xhr.status !== 200 && xhr.status !== 204) {
        onFail()
        return
      }
      console.warn('File upload success for ', this.file.name, xhr.status, xhr.responseText)
      this.paraEl.style.color = 'green'
      this.paraEl.innerText = 'Upload success :)'
      callback()
    }

    // Build and send form
    xhr.open("POST", this.s3SignatureData.url)
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
}


const buildQuerystring = qs => Object.keys(qs)
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(qs[key]))
    .join('&')
