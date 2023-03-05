const toggleHidden = () => {
    element = document.getElementById('hidden')
    if (element.style.color == 'rgb(29, 35, 48)') {
        element.style.color = '#fff'
    } else {
        element.style.color = '#1d2330'
    }
}