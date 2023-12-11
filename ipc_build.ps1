param(
    [switch]$generate = $false,
    [switch]$build_dep = $false,
    [switch]$compile_proto = $false
)


if($build_dep){
    Write-Host "Building dependencies"
    .\ipc_dependencies_build.ps1 -generate
    .\ipc_grpc_build.ps1 -generate -compile_proto
}else{
    Write-Host "Skipping building dependencies"
    .\ipc_grpc_build.ps1 -generate:$generate -compile_proto:$compile_proto
}

