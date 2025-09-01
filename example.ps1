# Run VcXsrv from saved config
Start-Process 'C:\Path\to\config.xlaunch'

# Wait a bit to ensure VcXsrv starts
Start-Sleep -Seconds 2

# Set DISPLAY variable for Docker
$env:DISPLAY = "host.docker.internal:0.0"

# Run the Docker container with ROS1
docker run -it --rm `
    -e DISPLAY=$env:DISPLAY `
    -v /tmp/.X11-unix:/tmp/.X11-unix `
    qcar-sim

# Kill VcXsrv after Docker container exits
Get-Process vcxsrv -ErrorAction SilentlyContinue | Stop-Process