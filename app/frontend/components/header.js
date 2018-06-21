import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'

import styles from 'styles/header.css'


class Header extends Component {

  static propTypes = {
    title: PropTypes.string.isRequired,
  }

  render()
  {
    const { title } = this.props
    return (
      <header className={styles.header}>
        <div className={styles.inner}>
          <Link to="/"><h1>{title}</h1></Link>
        </div>
      </header>
    )
  }
}


const mapStateToProps = state => ({
  title: state.title,
})
const mapDispatchToProps = dispatch => ({
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Header)
