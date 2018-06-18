import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Switch, Route, Link } from 'react-router-dom'

import styles from 'styles/header.css'


class Header extends Component {

  static propTypes ={
  }

  render()
  {
    const { } = this.props
    return (
      <header className={styles.header}>
        <h1>Memories Ninja</h1>
      </header>
    )
  }
}


const mapStateToProps = state => ({
})
const mapDispatchToProps = dispatch => ({
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Header)
