import os
from tqdm import tqdm
from PIL import Image
import imagehash
import matplotlib.pyplot as plt
from utils import transfer_images

def compute_hash(image_path):
    """
    Compute the average hash for an image.
    """
    try:
        with Image.open(image_path) as img:
            return imagehash.average_hash(img)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def cluster_images(image_paths, threshold=5):
    """
    Cluster images by comparing perceptual hashes.
    
    Parameters:
    - image_paths: List of paths to images.
    - threshold: Maximum Hamming distance for images to be considered similar.
    
    Returns:
    - List of clusters, each cluster is a list of image paths.
    """
    clusters = []
    
    pbar = tqdm(image_paths, ncols=150)
    for path in pbar:
        img_hash = compute_hash(path)
        if img_hash is None:
            continue  # Skip images that failed to process
        
        # Flag to indicate if the image has been added to an existing cluster.
        added = False
        for cluster in clusters:
            # Use the first image's hash in the cluster as its representative.
            rep_hash = cluster['rep_hash']
            if abs(img_hash - rep_hash) < threshold:
                cluster['images'].append(path)
                added = True
                break
        
        # If image didn't match any existing cluster, create a new cluster.
        if not added:
            clusters.append({
                'rep_hash': img_hash,
                'images': [path]
            })
    
    # Extract only the image lists from each cluster for easier use.
    return [cluster['images'] for cluster in clusters]

def visualize_clusters(clusters, max_images_per_cluster=6, output_dir="clusters"):
    """
    Visualize each cluster by displaying a few sample images.
    
    Parameters:
      clusters: List of clusters, each is a list of image paths.
      max_images_per_cluster: Maximum number of images to display per cluster.
      output_dir: Directory to save the visualizations.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, cluster in enumerate(clusters):
        n_images = min(len(cluster), max_images_per_cluster)
        fig, axes = plt.subplots(1, n_images, figsize=(15, 5))
        fig.suptitle(f'Cluster {idx + 1} ({len(cluster)} images)', fontsize=16)
        if n_images == 1:
            axes = [axes]  # Ensure axes is iterable even for a single subplot
        
        for ax, image_path in zip(axes, cluster[:n_images]):
            try:
                img = Image.open(image_path)
                ax.imshow(img)
                ax.set_title(os.path.basename(image_path), fontsize=8)
                ax.axis('off')
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
        plt.tight_layout()
        plt.show()

        output_file = os.path.join(output_dir, f"cluster_{idx+1}.png")
        plt.savefig(output_file)
        print(f"Saved cluster visualization to: {output_file}")
        plt.close(fig)
        

if __name__ == "__main__":
    image_folder = "/media/appuser"
    visualize_flag = os.getenv("VISUALIZE_CLUSTER", "false").lower() in ["true", "1", "yes"]
    transfer_flag = os.getenv("TRANSFER_IMAGES", "false").lower() in ["true", "1", "yes"]

    if visualize_flag:
        print(os.getenv("VISUALIZE_CLUSTER"))

    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    image_files = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(valid_extensions)
    ]
    
    clusters = cluster_images(image_files, threshold=1)
    print(f"Found {len(clusters)} clusters.")
    
    # Visualize the clusters
    if visualize_flag:
        visualize_clusters(clusters, max_images_per_cluster=6, output_dir="/media/appuser/clusters")
    
    if transfer_flag:
        transfer_images(clusters, destination_folder="/media/appuser/archive")



