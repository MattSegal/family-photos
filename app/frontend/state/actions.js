import api from './api'

module.exports = {
  // Redux's store.dispatch is aliased to 'd' for brevity
  fetchAlbum: id => d => {
    d({type: 'REQUEST_API'})
    return api.album.get(id)
      .then( r => r.data)
      .then( data => d({type: 'RECEIVE_ALBUM', data: data}))
      .catch((error) => {
        console.error(error)
        d({type: 'API_ERROR'})
      })
  },
  listAlbums: () => d => {
    d({type: 'REQUEST_API'})
    return api.album.list()
      .then( r => r.data)
      .then( data => d({type: 'RECEIVE_ALBUMS', data: data}))
      .catch((error) => {
        console.error(error)
        d({type: 'API_ERROR'})
      })
  },
  setTitle: title => ({type: 'SET_TITLE', title: title}),
}
