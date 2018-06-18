import api from './api'


module.exports = {
  // Redux's store.dispatch is aliased to 'd' for brevity
  listAlbums: () => d => {
    d({type: 'REQUEST_ALBUMS'})
    return api.album.list()
      .then( r => r.data)
      .then( data => d({type: 'RECEIVE_ALBUMS', data: data}))
      .catch( error => {
        d({type: 'ERROR_ALBUMS'})
      })
  },
}
