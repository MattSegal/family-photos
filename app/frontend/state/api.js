import axios from 'axios'
import Cookies from 'js-cookie'

module.exports = {
  album: {
    get: id => axios({
      url: `/api/album/${id}/`,
      method: 'get',
    }),
    list: () => axios({
      url: '/api/album/',
      method: 'get',
    }),
  },
  image: {
    upload: image => {
      const form  = new FormData()
      form.append('csrfmiddlewaretoken', Cookies.get('csrftoken'))
      form.append('local_file', image.file)
      form.append('title', image.name)
      form.append('album', image.album.id)
      return axios({
        url: '/upload/',
        method: 'post',
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        data: form,
      })
  },
  }
}
