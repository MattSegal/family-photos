import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Provider } from 'react-redux'

import { store } from 'state'
import Header from 'components/header'
import AlbumList from 'components/album-list'

class App extends Component {

  render() {
    return (
      <Provider store={store}>
        <div>
            <Header/>
            <AlbumList/>
        </div>
      </Provider>
    )
  }
}


ReactDOM.render(<App/>, document.getElementById('app'))
