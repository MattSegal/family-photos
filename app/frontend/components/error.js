import React, { Component } from 'react'

import styles from 'styles/error.css'


export default class ErrorBoundary extends Component {

  constructor(props) {
    super(props)
    this.state = {
      hasError: false,
    }
  }

  componentDidCatch(error, info) {
    console.error(error, info)
    this.setState({ hasError: true })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.noRender) {
        return null
      }
      return (
        <div className={styles.error}>
          <h2>Something broke >:(</h2>
        </div>
      )
    }
    return this.props.children
  }
}
