import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { actions } from 'state'

import styles from 'styles/modal.css'

class ImageModalInner extends Component {

  constructor(props) {
    super(props)
    this.state = {
      loading: false,
      loaded: []
    }
  }

  componentDidMount() {
    // Lock body scroll
    const body = document.getElementsByTagName('body')[0]
    body.setAttribute('style', 'overflow: hidden;')
    setTimeout(() => this.setState({ loading: true }), 200)
  }

  componentWillUnmount() {
    // Unlock body scroll
    const body = document.getElementsByTagName('body')[0]
    body.setAttribute('style', '')
  }

  handleScroll = direction => {
    const { scrollModal } = this.props
    this.setState({ loading: true })
    scrollModal(direction)
  }

  onLoad = e => {
    const { images, imageIdx } = this.props
    const src = images[imageIdx].display_url
    this.setState({
      loading: false,
      loaded: [...this.state.loaded, src]
    })
  }

  render() {
    const { images, imageIdx, closeModal } = this.props
    const src = images[imageIdx].display_url
    const loaded = this.state.loaded.includes(src)
    const loadingText = this.state.loading
    return (
      <div className={styles.modal}>
        <div onClick={closeModal} className={styles.close}>&times;</div>
        <div
          onClick={() => this.handleScroll(1)}
          className={styles.right}>
            &gt;
        </div>
        <div
          onClick={() => this.handleScroll(-1)}
          className={styles.left}>
            &lt;
        </div>
        <div className={`${styles.loading} ${loadingText && styles.loadingVisible}`}>
          Loading...
        </div>
        <div className={styles.counter}>
          {imageIdx + 1} / {images.length}
        </div>
        <img
          onLoad={this.onLoad}
          className={`${styles.image} ${loaded && styles.imageLoaded}`}
          src={src}
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
