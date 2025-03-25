import os
import shutil
from tqdm import tqdm

def cleanup_every_n_th(image_files, nth=5):
    pbar = tqdm(image_files, ncols=125)
    for i, image_file in enumerate(pbar):
        # (i+1) % 5 == 0 ensures that the 5th, 10th, 15th, ... images are deleted.
        if (i + 1) % nth == 0:
            pbar.set_description(f"Deleting: {image_file}")
            os.remove(image_file)

def transfer_images(clusters, destination_folder):
    """
    Given a list of clusters (each cluster is a list of image paths),
    this function transfers duplicate images (all except the representative) 
    to the destination folder.

    Parameters:
      clusters: List of clusters, where each cluster is a list of file paths.
      destination_folder: The folder where duplicate images will be moved.
    """
    # Create the destination folder if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    pbar = tqdm(clusters, ncols=125)
    for cluster in pbar:
        if not cluster:
            continue

        representative = cluster[0]
        pbar.set_description(f"Keeping representative: {representative}")

        for image_path in cluster[1:]:
            try:
                dest_path = os.path.join(destination_folder, os.path.basename(image_path))
                # tqdm.write(f"Transferring duplicate: {image_path} -> {dest_path}")
                shutil.move(image_path, dest_path)
            except Exception as e:
                print(f"Error transferring {image_path}: {e}")