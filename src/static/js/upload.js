UPLOAD_URL = '/api/upload'

// Uploader states
STATES = {
  SELECT: 0,
  UPLOADING: 1,
  UPLOADED: 2,
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
    this.uploadedImageCount = 0
    
    // Ensure files selected
    this.setState(STATES.SELECT)
    if (!files.length > 0) return
    this.setState(STATES.SIGNATURE)

    for (let idx = 0; idx < files.length; idx++) {
      this.imageUploads.push(new ImageUpload(files[idx], this.uploadListEl))
    }

    // Upload each image in parallel
    this.imageUploads.forEach(i => i.upload(this.onUploadFinished.bind(this)))
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

    this.divEl = document.createElement("div")
    this.divEl.classList.add('upload-image')
    this.paraEl = document.createElement("p")

    this.imageEl = new Image()
    this.imageEl.height = 140
    this.imageEl.onload = () => uploadListEl.appendChild(this.divEl)
    
    this.divEl.appendChild(this.imageEl)
    this.divEl.appendChild(this.paraEl)

    this.imageEl.src =  URL.createObjectURL(this.file)
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
}
