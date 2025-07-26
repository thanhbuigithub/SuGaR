import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup the environment')
    
    parser.add_argument('--no_nvdiffrast', action='store_true', help='Skip installation of Nvdiffrast')
    args = parser.parse_args()
    
    # Create a new conda environment
    print("[INFO] Creating the conda environment for SuGaR...")
    os.system("conda env create -f environment.yml")
    print("[INFO] Conda environment created.")

    # Install cudatoolkit
    print("[INFO] Installing cudatoolkit...")
    os.system("conda run -n sugar conda install cuda cudatoolkit=11.8 -c nvidia/label/cuda-11.8.0 -y")
    print("[INFO] cudatoolkit installed.")

    print(f"[DEBUG] Current TORCH_CUDA_ARCH_LIST: {os.environ.get('TORCH_CUDA_ARCH_LIST')}")
    os.environ["TORCH_CUDA_ARCH_LIST"] = "8.6"
    print(f"[INFO] Set TORCH_CUDA_ARCH_LIST to: {os.environ['TORCH_CUDA_ARCH_LIST']}")
    
    print("[INFO] Installing gcc_linux-64 and gxx_linux-64 in the 'sugar' conda environment...")
    os.system("conda run -n sugar conda install -c conda-forge gcc_linux-64 gxx_linux-64 -y")
    print("[INFO] gcc_linux-64 and gxx_linux-64 installed.")
    
    # Install 3D Gaussian Splatting rasterizer
    print("[INFO] Installing the 3D Gaussian Splatting rasterizer...")
    os.chdir("gaussian_splatting/submodules/diff-gaussian-rasterization/")
    os.system("conda run -n sugar pip install -e .")
    print("[INFO] 3D Gaussian Splatting rasterizer installed.")
    
    # Install simple-knn
    print("[INFO] Installing simple-knn...")
    os.chdir("../simple-knn/")
    os.system("conda run -n sugar pip install -e .")
    print("[INFO] simple-knn installed.")
    os.chdir("../../../")
    
    # Install Nvdiffrast
    if args.no_nvdiffrast:
        print("[INFO] Skipping installation of Nvdiffrast.")
    else:
        print("[INFO] Installing Nvdiffrast...")
        os.system("git clone https://github.com/NVlabs/nvdiffrast")
        os.chdir("nvdiffrast")
        os.system("conda run -n sugar pip install .")
        print("[INFO] Nvdiffrast installed.")
        print("[INFO] Please note that Nvdiffrast will take a few seconds or minutes to build the first time it is used.")
        os.chdir("../")

    print("[INFO] SuGaR installation complete.")
