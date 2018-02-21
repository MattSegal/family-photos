$albumSelect = $('select')
$fileUpload = $('.file-upload')

$uploadList = $('#upload-list')
$uploadForm = $('#upload-form')
$progressHolder = $('.progress-holder')

$uploadBar = $('.progress-bar.upload')
$uploadMessage = $('.upload-message.upload')

$errorBar = $('.progress-bar.error')
$successBar = $('.progress-bar.success')
$successMessage = $('.upload-message.success')

const $getUploadItem = file => $uploadList.children("[data-name='" + file.name + "']")

let countSubmitted = 0
let countSuccess = 0
let countError = 0
let hasBeenWarned = false

$albumSelect.change(e => $fileUpload.removeClass('hidden'))

const handleSubmit = file => {
  countSubmitted += 1
  $uploadMessage.text('Uploading ' + countSubmitted + ' files')
}


const handleSuccess = file => {
  countSuccess += 1
  $successMessage.text(countSuccess + ' successful, ' + countError + ' failed')
  $successBar.css('width', 100 * countSuccess / countSubmitted + '%')
  let $uploadItem = $getUploadItem(file)
  $uploadItem.find('p').text('Success')
}


const handleError = file => {
  countError += 1
  $successMessage.text(countSuccess + ' successful, ' + countError + ' failed')
  $errorBar.css('width', 100 * countError / countSubmitted + '%')
  let $uploadItem = $getUploadItem(file)
  $uploadItem.find('p').text('Failed')
}


const onProgress = (e, data) => {
  $uploadBar.css('width', 100 * data.loaded / data.total + '%')
}


const onSubmit = (e, data) => {
  if (!$albumSelect.val()) {
    if (!hasBeenWarned) {
      alert('Select an album')
      hasBeenWarned = true
    }
    return false
  }
  if (data.files.length > 1) {
    console.error('More than one data file - ', data.files)
    return false
  }

  $uploadForm.addClass('hidden')
  $progressHolder.removeClass('hidden')

  let file = data.files[0]

  console.warn('Submitted', file.name)
  handleSubmit(file)
  let $uploadItem = $getUploadItem(file)
  if ($uploadItem.length > 0) {
    return
  }

  const src = URL.createObjectURL(file)
  $uploadItem = $('<div></div>')
    .addClass('upload-image')
    .attr('data-name', file.name)

  let $img = $('<img>').attr('height', 140).attr('src', src)
  $uploadItem.append($img)
  $uploadItem.append('<p>Uploading</p>')
  $uploadList.append( $uploadItem)
}


const onDone = (e, data) => {
  const file = data.files[0]
  let $uploadItem = $uploadList.children("[data-name='" + file.name + "']")
  let response =  data._response.result

  if (response.is_valid) {
    handleSuccess(file)
  } else {
    console.error('Failure uploading', file.name, ' - ', response.errors)
    handleError(file)
  }
}


const onFail = (e, data) => {
  const file = data.files[0]
  console.error('Failure uploading', file.name, ' - ', data.errorThrown)
  handleError(file)
}


// https://github.com/blueimp/jQuery-File-Upload/wiki/Options
$('#upload-form').fileupload({
  // Configuration
  type: 'POST',
  sequentialUploads: true,
  dataType: 'json',
  url: '/upload/',
  paramName: 'file',
  // Event handlers
  submit: onSubmit,
  done: onDone,
  fail: onFail,
  progressall: onProgress,
})
