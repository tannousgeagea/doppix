# Doppix

Doppix is a lightweight tool for deduplicating and clustering images using conventional image processing techniques. It leverages perceptual hashing to group similar images—making it easy to clean up large image collections without any AI.

## Features

- **Conventional Methods:** Uses average hashing (aHash) to capture the visual essence of an image.
- **Efficient Clustering:** Groups images by comparing hash values with a configurable Hamming distance threshold.
- **Minimal Dependencies:** Built with Python using simple libraries like Pillow and imagehash.
- **Easy Setup:** Designed to work out-of-the-box for batch processing large datasets.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/doppix.git
   cd doppix


2. **Install Dependencies:**

    Ensure you have docker installed. Then run:
    ```bash
    docker compose build

## Usage

### Prepare Your Images:
Place your images in a directory. Update the `image_folder` variable in the script (e.g., `doppix.py`) to point to your images folder.

### Run the Script:
Execute the script to start clustering:

    ```bash
    python3 main.py
    
## Review the Output:
The script will output the clusters with each group containing paths to similar images.

## Configuration

### Threshold Adjustment:

The script uses a Hamming distance threshold (default is 5) to determine similarity. Adjust this value in the cluster_images function as needed to fine-tune clustering sensitivity.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.
