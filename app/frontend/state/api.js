import axios from 'axios'
import Cookies from 'js-cookie'

module.exports = {
  album: {
    list: () => axios({
      url: '/api/album/',
      method: 'get',
    }),
  }
}
