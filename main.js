const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const { spawn } = require('child_process')
const path = require('path')

var mainWindow
var startServer
var serverPort

app.on('ready', () => {
    
    // open server
    const pythonFile = path.join(__dirname, 'server', 'main.py')
    startServer = spawn('python', [pythonFile])

    startServer.stdout.on('data', (data) => {
        
        try {
            serverPort = data.toString().trim().split("PORT=")[1].split('\n')[0].trim()

            // main window creation
            mainWindow = new BrowserWindow({
                webPreferences:{
                    nodeIntegration: true,
                    contextIsolation: false,
                    devTools: true
                },
                width: 955,
                height: 600,
                resizable:true,
                minWidth:700,
                minHeight:440,
                transparent:false,
                frame:false,
            })

            //mainWindow.loadURL(`File://${__dirname}/ui/templates/index.html`)
            mainWindow.loadURL(`http://localhost:${serverPort}`)

            // Listener para abrir o file browser
            ipcMain.handle('open-file-dialog', async () => {
                const result = await dialog.showOpenDialog(mainWindow, {
                    properties: ['openFile'],
                    filters: [
                        { name: 'file', extensions: ['wav', 'mp3', 'png', 'jpeg'] }
                    ]
                })
                return result.filePaths[0] || null
            })

            // Listen for the maximize event
            mainWindow.on('maximize', () => {
                console.log('Window maximized')
                mainWindow.webContents.send('window-maximized')
            })
            mainWindow.on('unmaximize', () => {
                console.log('Window unmaximized')
                mainWindow.webContents.send('window-unmaximized')
            })

            ipcMain.on('close', (e, csrf) => {
                mainWindow.close()
            })

            app.on('window-all-closed', () => {
                if (process.platform !== 'darwin') {
                    app.quit()
                }

            })

            // kill python process
            app.on('before-quit', () => {
                startServer.kill()
            })
            mainWindow.on('closed', () => {
                if (startServer) {
                    startServer.kill()
                }
                mainWindow = null
            })

        } catch(e){
            console.log(`port error. ${e}`)
        }
    })
})
