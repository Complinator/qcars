# Run VcXsrv from saved config
Start-Process 'C:\Path\to\your\config.xlaunch'

# Wait a bit to ensure VcXsrv starts
Start-Sleep -Seconds 2

# Set DISPLAY variable for Docker
$env:DISPLAY = "host.docker.internal:0.0"

# Run the Docker container
docker run -it --rm `
    -e DISPLAY=$env:DISPLAY `
    -v /tmp/.X11-unix:/tmp/.X11-unix `
    --network host `
    --name qcar_sim `
    qcar_sim bash

# Kill VcXsrv after Docker container exits
Get-Process vcxsrv -ErrorAction SilentlyContinue | Stop-Process