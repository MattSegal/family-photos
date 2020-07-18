import React, { Component } from 'react'
import PropTypes from 'prop-types'

import styles from './select.css'


export default class SelectInput extends Component {

  static propTypes = {
    onChange: PropTypes.func.isRequired,
    prompt: PropTypes.string.isRequired,
    selected: PropTypes.any,
    disabled: PropTypes.bool,
    options: PropTypes.arrayOf(PropTypes.shape({
      value: PropTypes.any,
      display: PropTypes.string,
    }))
  }

  handleChange = e => {
    this.props.onChange(e.target.value)
  }

  render()
  {
    return (
      <select
        disabled={this.props.disabled}
        className={styles.select}
        onChange={this.handleChange}
        value={this.props.selected || ''}
      >
        <option value="">{this.props.prompt}</option>
        {this.props.options.map(({ value, display }, idx) =>
          <option key={idx} value={value}>{display}</option>
        )}
      </select>
    )
  }
}
