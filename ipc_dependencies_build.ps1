git submodule update --init --recursive

cd src

mkdir build_grpc
cd build_grpc
cmake ../grpc -G "Ninja" -DCMAKE_BUILD_TYPE=Debug


cmake --build . --config Debug

mkdir install_grpc
cmake --install . --config Debug --prefix "$pwd/install_grpc"

cd ..

mkdir build_opencv
cd build_opencv
cmake ../opencv -G "Ninja" -DCMAKE_BUILD_TYPE=Debug -DOpenCV_STATIC=ON

cmake --build . --config Debug

mkdir install_opencv
cmake --install . --prefix "$pwd/install_opencv" --config Debug

cd ..
cd ..