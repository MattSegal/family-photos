import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'
import Thumbnail from 'components/thumbnail'

import styles from 'styles/album.css'

const FOUND = 'FOUND'
const NOT_FOUND = 'NOT_FOUND'
const DATA_NOT_FETCHED_YET = 'DATA_NOT_FETCHED_YET'


class Album extends Component {

  static propTypes = {
    pageLoaded: PropTypes.func.isRequired,
    showModal: PropTypes.func.isRequired,
    setTitle: PropTypes.func.isRequired,
    listAlbums: PropTypes.func.isRequired,
    fetchAlbum: PropTypes.func.isRequired,
    loadedPages: PropTypes.arrayOf(PropTypes.string),
    slug: PropTypes.string.isRequired,
    albums: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        slug: PropTypes.string.isRequired,
        num_photos: PropTypes.number.isRequired,
        photos: PropTypes.arrayOf(
          PropTypes.shape({
            id: PropTypes.number.isRequired,
            taken_at: PropTypes.string.isRequired,
            display_url: PropTypes.string.isRequired,
            thumb_url: PropTypes.string.isRequired,
          }).isRequired,
        )
      })
    )
  }

  constructor(props) {
    super(props)
    this.state = this.findAlbum()
  }

  findAlbum() {
    const { albums, slug } = this.props
    const album = albums.find(album => album.slug == slug)
    let status
    if (album) { status = FOUND }
    else if (albums.length < 1) { status = DATA_NOT_FETCHED_YET }
    else { status = NOT_FOUND }
    return {
      status: status,
      album: album,
    }
  }

  componentDidMount() {
    window.scrollTo(0, 0)
    if (this.state.status === DATA_NOT_FETCHED_YET) {
      this.props.listAlbums()
      .then(() => {
        const { status, album } = this.findAlbum()
        this.setState({
          status: status,
          album: album,
        })
        if (this.state.status === FOUND) {
          this.props.setTitle(album.name)
          this.props.fetchAlbum(album.id)
          .then(() => this.setState(this.findAlbum()))
        }
      })
    } else if (this.state.status === FOUND) {
      const { album } = this.state
      this.props.setTitle(album.name)
      this.props.fetchAlbum(album.id)
      .then(() => this.setState(this.findAlbum()))
    } else if (this.state.status === NOT_FOUND) {
      // Do nothing
    }
    setTimeout(() => this.props.pageLoaded(this.props.slug), 3000)
  }

  render() {
    const { loadedPages, slug } = this.props
    const { album, status } = this.state
    const loaded = loadedPages.includes(slug)
    if (status === NOT_FOUND || status === DATA_NOT_FETCHED_YET) {
      return null
    }
    const showModal = this.props.showModal(album.photos)
    return (
      <div className={styles.album}>
        <div className={styles.photos}>
          {album.photos.map((photo, idx) =>
            <Thumbnail key={idx} {...photo} showModal={showModal} loaded={loaded}/>
          )}
          {Array(album.num_photos - album.photos.length).fill(0).map((zero, idx) =>
            <Thumbnail key={album.photos.length + idx}/>
          )}
        </div>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  albums: state.albums,
  loadedPages: state.loadedPages,
})
const mapDispatchToProps = dispatch => ({
    pageLoaded: page => dispatch(actions.pageLoaded(page)),
    fetchAlbum: (id) => dispatch(actions.fetchAlbum(id)),
    listAlbums: () => dispatch(actions.listAlbums()),
    setTitle: title => dispatch(actions.setTitle(title)),
    showModal: images => imageId => dispatch(actions.showModal(imageId, images)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Album)
