import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from './button.css'


export default class Button extends Component {

  static propTypes = {
    onClick: PropTypes.func.isRequired,
    text: PropTypes.string.isRequired,
    disabled: PropTypes.bool,
  }

  static defaultProps = {
    disabled: false,
  }

  render()
  {
    return (
      <button
        className={styles.button}
        onClick={this.props.onClick}
        disabled={this.props.disabled}
      >
        {this.props.text}
      </button>
    )
  }
}
