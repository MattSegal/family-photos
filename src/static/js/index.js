// TODO - little left and right arrows
// todo - eagerly fetch left and right images

const ESC_KEY = 27
const LEFT_ARROW = 37
const RIGHT_ARROW = 39
const imgs = document.getElementsByTagName('img')

const displayImage = document.getElementById('display-image')
const displayModal = document.getElementById('display-modal')

const numImages = imgs.length
let currentImage = 0

const setDisplayImage = i => {
    displayImage.src = imgs[i].src.replace('/thumbnail/', '/display/')
}
const inRange = i => i >= 0 && i < numImages

const removeModal = () => {
    displayModal.classList.remove('visible')
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