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
  }
}
