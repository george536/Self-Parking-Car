param(
    [switch]$generate = $false
)

#git submodule update --init --recursive # run yourself or maybe make it into a flag?

if($generate){
    Write-Host "Generating project files"
}else
{
    Write-Host "Skipping generation of project files"
}

cd src


pip install grpcio-tools

mkdir build_grpc
cd build_grpc

if($generate){
    cmake ../grpc -G "Ninja" -DCMAKE_BUILD_TYPE=Debug
}



cmake --build . --config Debug

mkdir install_grpc
cmake --install . --config Debug --prefix "$pwd/install_grpc"

cd ..

mkdir build_opencv
cd build_opencv

if($generate)
{
    cmake ../opencv -G "Ninja" -DCMAKE_BUILD_TYPE=Debug -DOpenCV_STATIC=ON
}

cmake --build . --config Debug

mkdir install_opencv
cmake --install . --prefix "$pwd/install_opencv" --config Debug

cd ..
cd ..

# Copying all .dll files needed for opencv
$sourcePath = "$pwd/src/build_opencv/bin"
$destinationPath = "$pwd/src/build"

# Copy all .dll files from the source to the destination folder
Get-ChildItem -Path $sourcePath -Filter "*.dll" | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $destinationPath
}

Write-Host "Copying .dll files to build folder has completed."