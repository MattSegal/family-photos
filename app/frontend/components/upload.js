import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'

import styles from 'styles/upload.css'


class Upload extends Component {

  static propTypes = {
    setTitle: PropTypes.func.isRequired,
  }

  componentDidMount() {
    window.scrollTo(0, 0)
    this.props.setTitle('Uploads')
  }

  render()
  {
    const { albums } = this.props
    // TODO - use spark MD5 to client side hash images
    // use file upload singleton or something?
    // don't let re-render destroy upload process
    // X / Y uploaded
    // Allow add files while uploading?
    // Ensure proper dedupe works
    // better upload validation (server side, client side)
    // more optimistic upload success
    // can browse or add more uploads while uploading
    // auto retry uploads
    // uploaded photos show nicer "not thumbnail" if not loading
    // validate JPEG content type client side
    //<script type="text/javascript" src="{% static 'js/vendor/jquery-1.9.1.min.js' %}"></script>
    //<script type="text/javascript" src="{% static 'js/vendor/jquery.ui.widget.js' %}"></script>
    //<script type="text/javascript" src="{% static 'js/vendor/jquery.fileupload.js' %}"></script>
    //https://github.com/MattSegal/family-photos/blob/master/app/photos/static/js/upload.js
    return (
      <div className={styles.wrapper}>
        <div className={styles.inner}>
          <select name="album" id="select-album" form="upload-form">
              <option value="">Select album</option>
              {albums.map((album, idx) =>
                <option key={idx} value={album.id}>{album.name}</option>
              )}
          </select>
          <input id="file-input" type="file" multiple/>
          <button>Upload</button>
        </div>
      </div>
    )
  }
}


const mapStateToProps = state => ({
  albums: state.albums,
})
const mapDispatchToProps = dispatch => ({
    setTitle: title => dispatch(actions.setTitle(title)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Upload)
