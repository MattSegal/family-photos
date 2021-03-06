// TODO - little left and right arrows

const ESC_KEY = 27
const LEFT_ARROW = 37
const RIGHT_ARROW = 39
const imgs = document.getElementsByClassName('thumb')

const html = document.getElementsByTagName('html')[0]
const displayImage = document.getElementById('modal-image')
const loadingText = document.getElementById('modal-loading')
const exitButton = document.getElementById('modal-exit')
const leftButton = document.getElementById('modal-left')
const rightButton = document.getElementById('modal-right')
const displayModal = document.getElementById('display-modal')

const numImages = imgs.length
let currentImage = 0

const inRange = i => i >= 0 && i < numImages
const removeModal = () => {
    html.style.overflow = 'auto'
    displayModal.classList.remove('visible')
    displayImage.src = '#'
}
const prefetchImage = url => (new Image()).src = url
const getDisplayURL = i => imgs[i].src.replace('/thumbnail/', '/display/')
const setDisplayImage = i => {
    displayImage.classList.add('loading')
    loadingText.classList.add('loading')
    displayImage.onload = e => {
        displayImage.classList.remove('loading')
        loadingText.classList.remove('loading')
    }
    displayImage.src = getDisplayURL(i)

    // Prefetch 4 surrounding images
    if (inRange(i - 2)) prefetchImage(getDisplayURL(i - 2))
    if (inRange(i - 1)) prefetchImage(getDisplayURL(i - 1))
    if (inRange(i + 1)) prefetchImage(getDisplayURL(i + 1))
    if (inRange(i + 2)) prefetchImage(getDisplayURL(i + 2))
}

const scrollLeft = () => {
    if (inRange(currentImage - 1)) {
        currentImage--
        setDisplayImage(currentImage)
    }
}
const scrollRight = () => {
    if (inRange(currentImage + 1)) {
        currentImage++
        setDisplayImage(currentImage)
    }
}


exitButton.onclick = removeModal
leftButton.onclick = scrollLeft
rightButton.onclick = scrollRight
document.onkeydown = (e) => {
    if (e.keyCode == ESC_KEY) {
        removeModal()
    } else if (displayModal.classList.contains('visible')) {
        if (e.keyCode === LEFT_ARROW) {
            scrollLeft()
        } else if (e.keyCode === RIGHT_ARROW) {
            scrollRight()
        }
    }
}

for (let i = 0; i < numImages; i++) {
    imgs[i].onclick = () => {
        displayModal.classList.add('visible')
        html.style.overflow = 'hidden'
        currentImage = i
        setDisplayImage(i)
    }
    const shade = Math.floor(200 + Math.random() * 55)
    imgs[i].style.backgroundColor = 'rgb('+shade+','+shade+','+shade+')'
}



// Handle left / right swipe - thanks Stack Overflow!
let xDown = null
let yDown = null

const handleTouchStart = e => {
    xDown = e.touches[0].clientX
    yDown = e.touches[0].clientY
}
const handleTouchMove = e => {
    if ( ! xDown || ! yDown ) return
    const xUp = e.touches[0].clientX
    const yUp = e.touches[0].clientY

    const xDiff = xDown - xUp
    const yDiff = yDown - yUp

    if ( 3 * Math.abs( xDiff ) > Math.abs( yDiff ) ) {
        if ( xDiff > 0 ) {
            /* left swipe */
            scrollRight()
        } else {
            /* right swipe */
            scrollLeft()
        }
    } else {
        if ( yDiff > 0 ) {
            /* up swipe */
        } else {
            /* down swipe */
        }
    }
    /* reset values */
    xDown = null
    yDown = null
}
document.ontouchstart = handleTouchStart
document.ontouchmove = handleTouchMove
