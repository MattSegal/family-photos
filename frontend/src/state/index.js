import { applyMiddleware, createStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger }  from 'redux-logger'

import reducer from './reducer'
import actions from './actions'
import listener from './listener';
import { uploadMiddleware } from './middleware'

const loggerMiddleware = createLogger()
const middleware = applyMiddleware(uploadMiddleware, thunkMiddleware, loggerMiddleware)

const initialiseState = data => ({
    settings: {
        thumbHeight: data.thumb_height,
        thumbWidth: data.thumb_width,
    },
    title: data.title,
    albums: data.albums,
    loadedPages: [],
    header: {
        trayOpen: false,
    },
    modal: {
        isOpen: false,
        imageIdx: 0,
        images: [],
    },
    upload: {
        album: '',
        images: [],
        uploadValid: false,
        uploading: false,
    },
})

// Store - assume we have bootstrapData available
console.log('Loading bootstrap data', bootstrapData)
const initialState = initialiseState(bootstrapData)
console.log('Set up initial state', initialState)
const store = createStore(reducer, initialState, middleware)

// Initialize event listener
listener(store.dispatch, store.getState)

module.exports = { store, actions }
