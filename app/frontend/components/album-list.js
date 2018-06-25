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
    pageLoaded: PropTypes.func.isRequired,
    setTitle: PropTypes.func.isRequired,
    listAlbums: PropTypes.func.isRequired,
    loadedPages: PropTypes.arrayOf(PropTypes.string),
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

  constructor(props) {
    super(props)
    this.seed = Math.random()
  }

  componentDidMount() {
    window.scrollTo(0, 0)
    this.props.setTitle('Memories Ninja')
    if (this.props.albums.length < 1) {
      this.props.listAlbums()
    }
    setTimeout(() => this.props.pageLoaded('/'), 3000)
  }

  render() {
    const { albums, loadedPages } = this.props
    const loaded = loadedPages.includes('/')
    return (
      <div className={styles.albumList}>
        {albums
          .filter(album => album.photos.length > 3)
          .map((album, idx) =>
            <Album key={idx} idx={idx} seed={this.seed} album={album} loaded={loaded} />
          )
        }
      </div>
    )
  }
}


class Album extends Component {

  getFilterStyle = () => {
    const angle = (
      (this.props.seed * 2 * Math.PI) +
      (this.props.idx * Math.PI / 2)
    ) % (2 * Math.PI)
    const colorWheel = new ColorWheel(angle, 0.7, 0.5)
    return {
      backgroundColor: colorWheel.asCSS()
    }
  }

  render() {
    const { album, loaded } = this.props
    return (
      <Link to={`/album/${album.slug}`}>
        <div className={styles.album}>
          <div className={styles.filter} style={this.getFilterStyle()}></div>
          <div className={styles.title}>{album.name}</div>
          {album.photos.slice(0, 4).map((p, i) =>
            <Thumbnail key={i} loaded={loaded} {...p}/>
          )}
        </div>
      </Link>
    )
  }
}


const mapStateToProps = state => ({
  albums: state.albums,
  loadedPages: state.loadedPages,
})
const mapDispatchToProps = dispatch => ({
  pageLoaded: page => dispatch(actions.pageLoaded(page)),
  listAlbums: () => dispatch(actions.listAlbums()),
  setTitle: title => dispatch(actions.setTitle(title)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(AlbumList)
