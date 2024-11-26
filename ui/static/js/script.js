// time sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// fetch save add track
function fetchSaveAddTrack() {
    document.getElementById('add-trk-submit').addEventListener('click', async (e)=> {
        e.preventDefault()
        var addTrkName = document.getElementById('add-trk-name').value
        var addTrkTag = document.getElementById('add-trk-tag').value
        var addTrkUrl = document.getElementById('div-url-path').innerText
        var addTrkImgurl = document.getElementById('div-img-url-path').innerText
        await fetch('/add-track', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ track_name: addTrkName, track_tag: addTrkTag, track_url: addTrkUrl, track_img: addTrkImgurl })
        })
        await fetchTracklist()
    })
}

function deleteTrack(track_id) {
    const dell = ( async ()=>{

        await fetch('/delete-track', {
            method:'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ "track_id": track_id })
        })
        await fetchTracklist()

    })()
}

// open add modal
function openAddModel () {
    document.querySelector('.btn-add').addEventListener('click', ()=> {
        document.querySelector('.modal-bg').style.opacity = '1'
        document.querySelector('.modal-bg').style.pointerEvents = 'all'
        document.querySelector('.modal-add').style.opacity = '1'
        document.querySelector('.modal-add').style.pointerEvents = 'all'
    })
}
function closeAddModal() {
    document.querySelector('.modal-bg').style.opacity = '0'
    document.querySelector('.modal-bg').style.pointerEvents = 'none'
    document.querySelector('.modal-add').style.opacity = '0'
    document.querySelector('.modal-add').style.pointerEvents = 'none'
}

function volumeSlider() {
    // input range style
    const slider = document.getElementById('range-vol-1')
    slider.addEventListener('input', () => {
        document.querySelector('.input-fill').style.width = `${slider.value}%`
    })
    const slider2 = document.getElementById('range-vol-2')
    slider2.addEventListener('input', () => {
        document.querySelector('.input-fill2').style.width = `${slider2.value}%`
    })
    // dis
    slider.addEventListener('wheel', (e)=> {
        return
        e.preventDefault()

        const step = slider.step ? parseFloat(slider.step) : 1

        if (e.deltaY < 0) {
            slider.value = Math.min(parseFloat(slider.value) + step, parseFloat(slider.max))
        } else {
            slider.value = Math.max(parseFloat(slider.value) - step, parseFloat(slider.min))
        }

        document.querySelector('.input-fill').style.width = `${slider.value}%`
    })
    slider.addEventListener('change', async () => {
        await fetch('/set-volume', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ "vol_out": slider.value, "vol_in": slider2.value })
        })
    })
    slider2.addEventListener('change', async () => {
        await fetch('/set-volume', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ "vol_out": slider.value, "vol_in": slider2.value })
        })
    })
}

function playAudio(url, device) {
    fetch('/play-audio', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ "url": url, "device": device })
    })
}

function startMic() {
    fetch('/start-audio-stream', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({  })
    })
    .then(response => {
        if (!response.ok) {throw new Error('error')}
        return response.json()
    })
    .then(data => {
        if (data.mic == true) {
            console.log(data.audio_stream)
            if (data.audio_stream != 'ok' || null) {
                document.querySelector('.btn-mic-in').classList.add('btn-mic-in-on-error')
                return
            }
            document.querySelector('.btn-mic-in').classList.add('btn-mic-in-on')
        }else{
            document.querySelector('.btn-mic-in').classList.remove('btn-mic-in-on')
        }
    })
}

function saveCfgInputDev(device) {
    fetch('/set-inputdev', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ "device": device })
    })
}
function saveCfgOutputDev(device) {
    fetch('/set-outputdev', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ "device": device })
    })
}

function getConfig() {
    fetch('/get-config', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({  })
    })
    .then(response => {
        if (!response.ok) {throw new Error('error')}
        return response.json()
    })
    .then(data => {
        document.getElementById('select-in-device').value = data.in_device
        document.getElementById('select-out-device').value = data.out_device
        document.getElementById('range-vol-1').value = data.vol_out
        document.getElementById('range-vol-2').value = data.vol_in
        document.querySelector('.input-fill').style.width = `${data.vol_out}%`
        document.querySelector('.input-fill2').style.width = `${data.vol_in}%`
    })
}

const fetchIdxContent = async ()=>{
    await sleep(1000)
    const response = await fetch('/index-content', {method:'POST', headers: {'X-CSRFToken': csrfToken} })
    const html = await response.text()
    document.querySelector('.div-main').innerHTML = html
}
// fetch index tracklist
const fetchTracklist = async ()=>{
    await sleep(1000)
    const response = await fetch('/track-list', {method:'POST', headers: {'X-CSRFToken': csrfToken} })
    const html = await response.text()
    document.querySelector('.list-track-ul').innerHTML = html
}

document.addEventListener("DOMContentLoaded", async ()=> {
    await fetchIdxContent()
    await fetchTracklist()
    getConfig()
    fetchSaveAddTrack()
    openAddModel()
    volumeSlider()
})