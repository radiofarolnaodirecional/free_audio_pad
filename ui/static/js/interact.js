function scrolBarFx(e, el) {
    const elWidth = el.offsetWidth
    const distance = elWidth - e.clientX

    console.log(distance)

    var scrollBarSize = 3 + (300 - distance) / 30

    if (scrollBarSize < 3) scrollBarSize = 3
    if (scrollBarSize > 8) scrollBarSize = 8

    document.documentElement.style.setProperty('--scrollbar-width', `${scrollBarSize}px`)

}
