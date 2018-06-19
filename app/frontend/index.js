import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Provider } from 'react-redux'

import { store } from 'state'
import Header from 'components/header'
import AlbumList from 'components/album-list'

import styles from 'styles/app.css'

class App extends Component {

  render() {
    return (
      <Provider store={store}>
        <div className={styles.app}>
            <Header/>
            <AlbumList/>
        </div>
      </Provider>
    )
  }
}


ReactDOM.render(<App/>, document.getElementById('app'))
