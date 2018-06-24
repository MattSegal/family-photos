import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Provider } from 'react-redux'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

import { store } from 'state'
import Header from 'components/header'
import AlbumList from 'components/album-list'
import Album from 'components/album'
import ErrorBoundary from 'components/error'
import ImageModal from 'components/modal'

import styles from 'styles/app.css'

class App extends Component {

  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <div className={styles.app}>
            <ErrorBoundary>
              <Header/>
            </ErrorBoundary>
            <Switch>
              <Route path="/album/:slug" component={({match}) =>
                <ErrorBoundary>
                  <Album slug={match.params.slug}/>
                </ErrorBoundary>
              }/>
              <Route path="/">
                <ErrorBoundary>
                  <AlbumList/>
                </ErrorBoundary>
              </Route>
            </Switch>
            <ErrorBoundary noRender={true}>
              <ImageModal/>
            </ErrorBoundary>
          </div>
        </BrowserRouter>
      </Provider>
    )
  }
}


ReactDOM.render(<App/>, document.getElementById('app'))
