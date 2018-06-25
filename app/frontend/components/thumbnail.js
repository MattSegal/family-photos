import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from 'styles/thumbnail.css'

// 1x1px transparent image
const DUMMY_IMAGE = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

export default class Thumbnail extends Component {

  static propTypes = {
    id: PropTypes.number,
    thumb_url: PropTypes.string,
    showModal: PropTypes.func,
    loaded: PropTypes.bool,
  }

  static defaultProps = {
    thumb_url: DUMMY_IMAGE,
    loaded: false
  }

  constructor(props) {
    super(props)
    this.state = {
      loaded: props.loaded
    }
  }

  handleLoad = e => {
    if (e.target.src !== DUMMY_IMAGE) {
      this.setState({ loaded: true })
    }
  }

  getShade = () => {
    const shade = Math.floor(220 + Math.random() * 35)
    return `rgb(${shade}, ${shade}, ${shade})`
  }

  getStyle = () => {
    return {
      opacity: this.state.loaded ? 0 : 1,
      backgroundColor: this.getShade(),
    }
  }

  render() {
    const showModal = this.props.showModal ?
      () => this.props.showModal(this.props.id) :
      () => {}
    return (
      <div className={styles.wrapper}>
        <div
          className={styles.preLoad}
          onClick={showModal}
          style={this.getStyle()}
        ></div>
        <img
          className={styles.thumbnail}
          src={this.props.thumb_url}
          onLoad={this.handleLoad}
          onClick={showModal}
        />
      </div>
    )
  }
}
