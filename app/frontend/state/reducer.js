// Reducers
const reducers = {
  REQUEST_ALBUMS: (state, action) => ({
    ...state,
  }),
  RECEIVE_ALBUMS: (state, action) => ({
    ...state,
    albums: action.data
  }),
  ERROR_ALBUMS: (state, action) => ({
    ...state,
  }),
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
