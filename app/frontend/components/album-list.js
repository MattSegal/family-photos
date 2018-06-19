import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'
import Thumbnail from 'components/thumbnail'
import ColorWheel from 'utils/color'
import styles from 'styles/album-list.css'


class AlbumList extends Component {

  static propTypes ={
    albums: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        slug: PropTypes.string.isRequired,
        top_photos: PropTypes.arrayOf(
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
    this.colorWheel = new ColorWheel(Math.random() * 2 * Math.PI, 0.6, 0.5)
  }

  componentDidMount() {
    this.props.listAlbums()
  }

  getFilterStyle = () => {
    this.colorWheel.rotate(2 * Math.PI / 3)
    return {
      backgroundColor: this.colorWheel.asCSS()
    }
  }

  render() {
    ColorWheel
    const { albums, settings } = this.props
    // TODO: Only show albums with 4+ photos
    return (
      <div className={styles.albumList}>
        { albums
          .filter(a => a.top_photos.length > 3)
          .map((a, idx) =>
            <div key={idx} className={styles.album}>
              <div className={styles.filter} style={this.getFilterStyle()}></div>
              <div className={styles.title}>{a.name}</div>
              {a.top_photos.map((p, i) =>
                <div key={i} className={styles.thumbnail}>
                  <Thumbnail {...p}/>
                </div>
              )}
            </div>
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
