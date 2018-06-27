import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'

import { actions } from 'state'

import styles from 'styles/header.css'


class Header extends Component {

  static propTypes = {
    toggleTray: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    trayOpen: PropTypes.bool.isRequired,
  }

  render()
  {
    const { title, toggleTray, trayOpen } = this.props
    return (
      <div className={styles.padding}>
      <header className={styles.header}>
        <div className={styles.inner}>
          <Link to="/"><h1>{title}</h1></Link>
          <div onClick={toggleTray} className={styles.hamburger}>
            <div className={styles.bar}></div>
            <div className={styles.bar}></div>
            <div className={styles.bar}></div>
          </div>
        </div>
        {trayOpen && (
          <div className={styles.tray}>
            <Link to="/" onClick={toggleTray}>
              <h3>Home</h3>
            </Link>
            <Link to="/upload/" onClick={toggleTray}>
              <h3>Uploads</h3>
            </Link>
          </div>
        )}
      </header>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  title: state.title,
  trayOpen: state.header.trayOpen,
})
const mapDispatchToProps = dispatch => ({
  toggleTray: () => dispatch(actions.toggleTray()),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Header)
