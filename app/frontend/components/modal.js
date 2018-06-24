import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'

import styles from 'styles/modal.css'


class ImageModalInner extends Component {

  componentDidMount() {
    // Lock body scroll
    const body = document.getElementsByTagName('body')[0]
    body.setAttribute('style', 'overflow: hidden;')
  }

  componentWillUnmount() {
    // Unlock body scroll
    const body = document.getElementsByTagName('body')[0]
    body.setAttribute('style', '')
  }

  render() {
    const { images, imageIdx, closeModal, scrollModal } = this.props
    return (
      <div className={styles.modal}>
        <div onClick={closeModal} className={styles.close}>&times;</div>
        <div
          onClick={() => scrollModal(1)}
          className={styles.right}>
            &gt;
        </div>
        <div
          onClick={() => scrollModal(-1)}
          className={styles.left}>
            &lt;
        </div>
        <div className={styles.loading}>Loading...</div>
        <img
          className={styles.image}
          src={images[imageIdx].display_url}
        />
      </div>
    )
  }
}


export default class ImageModal extends Component {

  static propTypes = {
    closeModal: PropTypes.func.isRequired,
    scrollModal: PropTypes.func.isRequired,
    isOpen: PropTypes.bool.isRequired,
    imageIdx: PropTypes.number.isRequired,
    images: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        display_url: PropTypes.string.isRequired,
      })
    ).isRequired,
  }

  static contextTypes = {
    router: PropTypes.shape({
      history: PropTypes.shape({
        listen: PropTypes.func,
      })
    })
  }

  prefetchImage = url => (new Image()).src = url

  componentDidUpdate(prevProps, prevState, snapshot) {
    // Prefetch images before and after current image
    const { imageIdx, images } = this.props
    // Prefetch previous image
    if (imageIdx > 0 && images.length > 1) {
      this.prefetchImage(images[imageIdx - 1].display_url)
    }
    // Prefetch next image
    if (imageIdx < images.length - 1) {
      this.prefetchImage(images[imageIdx + 1].display_url)
    }
  }

  componentDidMount() {
     const { router } = this.context
    if (router) {
      this.unlisten = router.history.listen(this.props.closeModal)
    }
  }

  componentWillUnmount() {
    if (this.unlisten) {
      this.unlisten()
    }
  }

  render() {
    const { isOpen } = this.props
    if (!isOpen) {
      return null
    }
    return <ImageModalInner {...this.props} />
  }
}


const mapStateToProps = state => ({
  isOpen: state.modal.isOpen,
  imageIdx: state.modal.imageIdx,
  images: state.modal.images,
})
const mapDispatchToProps = dispatch => ({
  closeModal: () => dispatch(actions.closeModal()),
  scrollModal: change => dispatch(actions.scrollModal(change)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(ImageModal)
