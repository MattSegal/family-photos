import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from './file.css'


export default class FileInput extends Component {

  static propTypes = {
    addFiles: PropTypes.func.isRequired,
    prompt: PropTypes.string.isRequired,
  }

  handleClick = e => this.input.click()
  handleChange = e => {
    const files = e.target.files
    if (files.length > 0) {
      this.props.addFiles(files)
      e.target.value = null
    }
  }

  render()
  {
    return (
      <div className={styles.file}>
        <input
          type="file"
          multiple
          onChange={this.handleChange}
          ref={r => { this.input = r; }}
        />
        <div onClick={this.handleClick}>{this.props.prompt}</div>
      </div>
    )
  }
}
