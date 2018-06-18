import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'


class AlbumList extends Component {

  static propTypes ={
    albums: PropTypes.array,
  }

  componentDidMount() {
    this.props.listAlbums()
  }

  render() {
    const { albums } = this.props
    console.warn(albums)
    return (
      <div>
        { albums.map((a, idx) =>
          <div key={idx}>{a.name}</div>
        )}
      </div>
    )
  }
}


const mapStateToProps = state => ({
    albums: state.albums,
})
const mapDispatchToProps = dispatch => ({
  listAlbums: () => dispatch(actions.listAlbums())
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(AlbumList)
