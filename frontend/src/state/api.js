const CSRF = document.querySelector('[name=csrfmiddlewaretoken]').value

module.exports = {
  album: {
    get: id =>
      fetch(`/api/album/${id}/`, { method: 'GET' })
      .then(r => r.json()),
    list: () =>
      fetch('/api/album/', { method: 'GET' })
      .then(r => r.json()),
  },
  image: {
    upload: image => {
      const form  = new FormData()
      form.append('csrfmiddlewaretoken', CSRF)
      form.append('local_file', image.file)
      form.append('title', image.name)
      form.append('album', image.album.id)
      return fetch('/upload/', {
        method: 'POST',
        credentials: 'include',
        headers: {'X-CSRFToken': CSRF},
        body: form,
      })
      .then(r => r.json())
    },
  }
}
