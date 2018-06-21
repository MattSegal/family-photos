// Reducers
const reducers = {
  SET_TITLE: (state, action) => ({
    ...state,
    title: action.title,
  }),
  RECEIVE_ALBUM: (state, action) => ({
    ...state,
    albums: state.albums.map(album => album.id === action.data.id ? action.data : album),
  }),
  RECEIVE_ALBUMS: (state, action) => ({
    ...state,
    albums: action.data,
  }),
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
