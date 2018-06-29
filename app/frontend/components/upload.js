import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'
import SelectInput from 'components/generic/select'
import FileInput from 'components/generic/file'
import Button from 'components/generic/button'

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
    // allow add a new album
    const { albums, album, uploadValid, images, uploading } = this.props
    return (
      <div className={styles.wrapper}>
        <div className={styles.inner}>
          <FormItem>
            <SelectInput
              onChange={this.props.selectAlbum}
              prompt="Select album"
              selected={ album.id }
              disabled={ uploading }
              options={ albums.map(a => ({value: a.id, display: a.name})) }
            />
          </FormItem>
          <FormItem>
            <FileInput
              prompt="Add images"
              addFiles={this.props.addImages}
            />
          </FormItem>
          <FormItem>
            <Button
              onClick={this.props.uploadImages}
              disabled={uploading || !uploadValid}
              text="Upload"
            />
            <Button
              onClick={this.props.clearImages}
              disabled={images.length < 1 || uploading}
              text="Clear"
            />
          </FormItem>
          {images.length > 0 && <div>
            <div className={styles.imageDetails}>
              {uploading
                ? (`Uploading ${images.length} images to "${album.name}".`)
                : (`${images.length} images selected.`)
              }
            </div>
            <div className={styles.imageList}>
              {images.map((i, idx) =>
                <div key={idx} className={`${styles.image} ${getImageStyle(i)}`}>
                  <img
                    height="100%"
                    width="100%"
                    src={i.src}
                  />
                </div>
              )}
            </div>
          </div>}
        </div>
      </div>
    )
  }
}

const getImageStyle = i => {
  if (i.state === 'SUCCESS') {
    return styles.success
  } else if (i.state === 'FAIL') {
    return styles.fail
  } else if (i.state === 'UPLOADING') {
    return styles.uploading
  }
}

const FormItem = props => <div className={styles.formItem}>{props.children}</div>


const mapStateToProps = state => ({
  albums: state.albums,
  uploadValid: state.upload.uploadValid,
  album: state.upload.album,
  images: state.upload.images,
  uploading: state.upload.uploading,
})
const mapDispatchToProps = dispatch => ({
    setTitle: title => dispatch(actions.setTitle(title)),
    selectAlbum: album => dispatch(actions.selectAlbum(album)),
    addImages: files => dispatch(actions.addImages(files)),
    uploadImages: () => dispatch(actions.uploadImages()),
    clearImages: () => dispatch(actions.clearImages()),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Upload)
