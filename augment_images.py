from PIL import Image
from torchvision import transforms
import argparse
import os
from multiprocessing import Pool, cpu_count

# Parse the arguments
parser = argparse.ArgumentParser(description="Augment images in a folder.")
parser.add_argument('--image_folder', type=str, default="images", help='Path to the image folder')
parser.add_argument('--output_folder', type=str, default="augmented_images", help='Path to the output folder')
parser.add_argument('--resolution', type=int, default=512, help='Resolution of the augmented images')
parser.add_argument('--num_augmentations', type=int, default=16, help='Number of augmentations per image')
parser.add_argument('--max_width_height_ratio_difference', type=float, default=.2, help='Only use images with that have a similar width and height')
args = parser.parse_args()

def augment_images(image: Image.Image, resolution: int, num_augmentations: int):
    augmentation_transforms = transforms.Compose(
        [
            transforms.Resize(resolution, interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.RandomCrop(resolution),
            transforms.RandomHorizontalFlip(),
        ]
    )
    
    augmented_images = []
    for _ in range(num_augmentations):
        augmented_image = augmentation_transforms(image)
        augmented_images.append(augmented_image)
    
    return augmented_images

def process_image(image_info):
    image_path, index = image_info
    image_filename = os.path.basename(image_path)
    image_extension = image_filename.split('.')[-1]
    
    # Open and convert the image once
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    width_height_ratio = width / height
    if width_height_ratio < 1-args.max_width_height_ratio_difference or width_height_ratio > 1+args.max_width_height_ratio_difference:
        return

    # Augment the image
    augmented_images = augment_images(image, resolution=args.resolution, num_augmentations=args.num_augmentations)
    
    # Save the augmented images
    for i, augmented_image in enumerate(augmented_images):
        image_number = index * args.num_augmentations + i
        augmented_image.save(f"{args.output_folder}/image_{image_number}.{image_extension}")

def main():
    # Create the output folder if it does not exist
    os.makedirs(args.output_folder, exist_ok=True)
    
    # Gather image file paths
    image_files = [(os.path.join(args.image_folder, entry.name), index)
                   for index, entry in enumerate(os.scandir(args.image_folder))
                   if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Process images in parallel
    with Pool(cpu_count()) as pool:
        pool.map(process_image, image_files)

if __name__ == "__main__":
    main()
