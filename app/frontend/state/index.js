import { applyMiddleware, createStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger }  from 'redux-logger'

import reducer from './reducer'
import actions from './actions'
import listener from './listener';

const loggerMiddleware = createLogger()
const middleware = applyMiddleware(thunkMiddleware, loggerMiddleware)

const initialiseState = data => ({
    settings: {
        thumbHeight: data.thumb_height,
        thumbWidth: data.thumb_width,
    },
    title: 'Memories Ninja',
    albums: [],
    modal: {
        isOpen: false,
        imageIdx: 0,
        images: [],
    }
})

// Store - assume we have bootstrapData available
console.log('Loading bootstrap data', bootstrapData)
const initialState = initialiseState(bootstrapData)
console.log('Set up initial state', initialState)
const store = createStore(reducer, initialState, middleware)

// Initialize event listener
listener(store.dispatch, store.getState)

module.exports = { store, actions }
