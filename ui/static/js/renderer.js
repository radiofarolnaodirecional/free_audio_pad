const { ipcRenderer } = require('electron')

// close app
async function closeApp(e) {
    try {
        await fetch('/close-server', {method:'POST', headers: {'X-CSRFToken': csrfToken} })
    }finally {
        ipcRenderer.send('close', csrfToken)
    }
}

// React to window maximized event
ipcRenderer.on('window-maximized', () => {
    divmain = document.querySelector('.div-main')
    bar = document.querySelector('.bar')
    divmain.style.borderRadius = '0'
    divmain.style.outline = '1px solid #0e0e0e'
    divmain.style.border = 'none'
    bar.style.borderRadius = '0'
    bar.style.outline = '1px solid black'
})
ipcRenderer.on('window-unmaximized', () => {
    divmain = document.querySelector('.div-main')
    bar = document.querySelector('.bar')
    divmain.style.borderRadius = '7px'
    divmain.style.outline = 'none'
    divmain.style.border = '1px solid #58c017'
    bar.style.borderRadius = '6px 6px 0 0'
    bar.style.outline = 'none'
})

// file browser
async function getLocalUrlPath(el) {
    const filePath = await ipcRenderer.invoke('open-file-dialog')
    if (filePath) {
        document.getElementById(`${el}`).innerText = `${filePath}`
    } else {
        document.getElementById(`${el}`).innerText = 'no path'
    }
}

document.getElementById("btnClose").addEventListener("click", closeApp)