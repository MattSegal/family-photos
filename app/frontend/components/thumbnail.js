import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from 'styles/thumbnail.css'


export default class Thumbnail extends Component {

  static propTypes = {
    id: PropTypes.number.isRequired,
    thumb_url: PropTypes.string.isRequired,
    showModal: PropTypes.func,
  }

  getShade = () => {
    const shade = Math.floor(200 + Math.random() * 55)
    return `rgb(${shade}, ${shade}, ${shade})`
  }

  getStyle = () => {
    return {
      backgroundColor: this.getShade(),
    }
  }

  render() {
    const showModal = this.props.showModal ?
      () => this.props.showModal(this.props.id) :
      () => {}
    return (
      <img
        className={styles.thumbnail}
        src={this.props.thumb_url}
        style={this.getStyle()}
        onClick={showModal}
      />
    )
  }
}
