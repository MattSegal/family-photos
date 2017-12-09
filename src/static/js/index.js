const imgs = document.getElementsByTagName('img')

const displayImage = document.getElementById('display-image')
const displayModal = document.getElementById('display-modal')

displayModal.onclick = () => displayModal.classList.remove('visible')

for (let i = 0; i < imgs.length; i++) {
    imgs[i].onclick = () => {
        // TODO - left/right scroll
        // TODO esc cancels image
        displayImage.src = imgs[i].src.replace('/thumbnail/', '/display/')
        displayModal.classList.add('visible')
    }
}