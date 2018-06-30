import Cookies from 'js-cookie'

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
      form.append('csrfmiddlewaretoken', Cookies.get('csrftoken'))
      form.append('local_file', image.file)
      form.append('title', image.name)
      form.append('album', image.album.id)
      return fetch('/upload/', {
        method: 'POST',
        credentials: 'include',
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        body: form,
      })
      .then(r => r.json())
    },
  }
}
