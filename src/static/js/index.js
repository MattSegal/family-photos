// TODO - little left and right arrows

const ESC_KEY = 27
const LEFT_ARROW = 37
const RIGHT_ARROW = 39
const imgs = document.getElementsByTagName('img')

const displayImage = document.getElementById('display-image')
const displayModal = document.getElementById('display-modal')

const numImages = imgs.length
let currentImage = 0

const inRange = i => i >= 0 && i < numImages
const removeModal = () => displayModal.classList.remove('visible')
const prefetchImage = url => (new Image()).src = url
const getDisplayURL = i => imgs[i].src.replace('/thumbnail/', '/display/')
const setDisplayImage = i => {
    displayImage.src = getDisplayURL(i)
    if (inRange(i - 1)) prefetchImage(getDisplayURL(i - 1))
    if (inRange(i + 1)) prefetchImage(getDisplayURL(i + 1))
}


displayModal.onclick = removeModal
document.onkeydown = (e) => {
    if (e.keyCode == ESC_KEY) {
        removeModal()
    } else if (displayModal.classList.contains('visible')) {
        if (e.keyCode === LEFT_ARROW && inRange(currentImage - 1)) {
            currentImage--
            setDisplayImage(currentImage)
        } else if (e.keyCode === RIGHT_ARROW && inRange(currentImage + 1)) {
            currentImage++
            setDisplayImage(currentImage)
        }
    }
}

for (let i = 0; i < numImages; i++) {
    imgs[i].onclick = () => {
        displayModal.classList.add('visible')
        currentImage = i
        setDisplayImage(i)
    }
}