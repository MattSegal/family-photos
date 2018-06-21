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
    setTitle: PropTypes.func.isRequired,
    listAlbums: PropTypes.func.isRequired,
    fetchAlbum: PropTypes.func.isRequired,
    slug: PropTypes.string.isRequired,
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
    } else {
      const { album } = this.state
      this.props.setTitle(album.name)
      this.props.fetchAlbum(album.id)
      .then(() => this.setState(this.findAlbum()))
    }
  }

  render() {
    const { album, status } = this.state
    if (status === NOT_FOUND) {
      return <div className={styles.message}><h2>Album not found</h2></div>
    } else if (status === DATA_NOT_FETCHED_YET) {
      return <div className={styles.message}><h2>Loading album...</h2></div>
    }
    return (
      <div className={styles.album}>
        <div className={styles.photos}>
          {album.photos.map((photo, idx) => <div key={idx}><Thumbnail {...photo} /></div>)}
        </div>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  albums: state.albums
})
const mapDispatchToProps = dispatch => ({
    fetchAlbum: (id) => dispatch(actions.fetchAlbum(id)),
    listAlbums: () => dispatch(actions.listAlbums()),
    setTitle: title => dispatch(actions.setTitle(title)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Album)
