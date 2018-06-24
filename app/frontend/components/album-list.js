import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'

import { actions } from 'state'
import Thumbnail from 'components/thumbnail'
import ColorWheel from 'utils/color'


import styles from 'styles/album-list.css'


class AlbumList extends Component {

  static propTypes = {
    setTitle: PropTypes.func.isRequired,
    listAlbums: PropTypes.func.isRequired,
    albums: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        slug: PropTypes.string.isRequired,
        photos: PropTypes.arrayOf(
          PropTypes.shape({
            id: PropTypes.number.isRequired,
            taken_at: PropTypes.string.isRequired,
            display_url: PropTypes.string.isRequired,
            thumb_url: PropTypes.string.isRequired,
          }),
        )
      })
    ),
  }

  componentDidMount() {
    this.props.setTitle('Memories Ninja')
    if (this.props.albums.length < 1) {
      this.props.listAlbums()
    }
  }

  render() {
    ColorWheel
    const { albums } = this.props
    return (
      <div className={styles.albumList}>
        {albums
          .filter(album => album.photos.length > 3)
          .map((album, idx) => <Album key={idx} {...album}/>)
        }
      </div>
    )
  }
}


class Album extends Component {

  constructor(props) {
    super(props)
    this.colorWheel = new ColorWheel(Math.random() * 2 * Math.PI, 0.6, 0.5)
  }

  getFilterStyle = () => {
    this.colorWheel.rotate(7 * Math.PI / 12)
    return {
      backgroundColor: this.colorWheel.asCSS()
    }
  }

  render() {
    const album = this.props
    return (
      <Link to={`/album/${album.slug}`}>
        <div className={styles.album}>
          <div className={styles.filter} style={this.getFilterStyle()}></div>
          <div className={styles.title}>{album.name}</div>
          {album.photos.slice(0, 4).map((p, i) =>
            <div key={i}>
              <Thumbnail {...p}/>
            </div>
          )}
        </div>
      </Link>
    )
  }
}


const mapStateToProps = state => ({
  albums: state.albums,
})
const mapDispatchToProps = dispatch => ({
  listAlbums: () => dispatch(actions.listAlbums()),
  setTitle: title => dispatch(actions.setTitle(title)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(AlbumList)
