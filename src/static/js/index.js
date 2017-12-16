// TODO - little left and right arrows

const ESC_KEY = 27
const LEFT_ARROW = 37
const RIGHT_ARROW = 39
const imgs = document.getElementsByTagName('img')

const html = document.getElementsByTagName('html')[0]
const displayImage = document.getElementById('display-image')
const displayModal = document.getElementById('display-modal')

const numImages = imgs.length
let currentImage = 0

const inRange = i => i >= 0 && i < numImages
const removeModal = () => {
    html.style.overflow = 'auto'
    displayModal.classList.remove('visible')
}
const prefetchImage = url => (new Image()).src = url
const getDisplayURL = i => imgs[i].src.replace('/thumbnail/', '/display/')
const setDisplayImage = i => {
    displayImage.src = getDisplayURL(i)
    if (inRange(i - 1)) prefetchImage(getDisplayURL(i - 1))
    if (inRange(i + 1)) prefetchImage(getDisplayURL(i + 1))
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


displayModal.onclick = removeModal
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

    if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {
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
