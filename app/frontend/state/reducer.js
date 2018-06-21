// Reducers
const reducers = {
  SET_TITLE: (state, action) => ({
    ...state,
    title: action.title,
  }),
  RECEIVE_ALBUM: (state, action) => ({
    ...state,
    albums: state.albums.map(album => {
      if (album.id !== action.data.id) {
        return album
      }
      return {
        ...album,
        ...action.data,
      }
    }),
  }),
  RECEIVE_ALBUMS: (state, action) => ({
    ...state,
    albums: action.data.map(album => ({
      ...album,
      photos: [],
    })),
  }),
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
