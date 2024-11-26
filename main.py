import os
from PIL import Image, ImageChops
from listing import Listing

def images_are_similar(img1, img2, threshold=0.65):
    # Calculate the difference between the images
    diff = ImageChops.difference(img1, img2)
    # Calculate the bounding box of the non-zero regions in the difference image
    bbox = diff.getbbox()
    if not bbox:
        return True  # Images are identical
    # Calculate the percentage of the image that is different
    diff_percentage = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) / (img1.size[0] * img1.size[1])
    return diff_percentage < threshold

def main():
    # toned = input("Are these slabs toned clad? (y/n): ")
    toned = "y"
    dir_of_slab_images = "./images"
    # first_image_is_blank = input("Is the first image blank? (y/n): ")
    first_image_is_blank = "n"
    # images_per_listing = int(input("How many images per listing? (Not including blanks)"))
    images_per_listing = 3
    blank_image = None
    listings = []
    current_listing_images = []

    for index, image_name in enumerate(os.listdir(dir_of_slab_images)):
        image_path = os.path.join(dir_of_slab_images, image_name)
        image = Image.open(image_path)

        if blank_image is None and first_image_is_blank.lower() == "y":
            blank_image = image
            continue

        if blank_image and images_are_similar(image, blank_image):
            continue

        current_listing_images.append(image_path)

        if len(current_listing_images) == images_per_listing:
            listings.append(Listing(images=current_listing_images))
            current_listing_images = []

    # Handle any remaining images that didn't form a complete listing
    if current_listing_images:
        listings.append(Listing(images=current_listing_images))
    print(listings)
    print(len(listings))
    return listings

if __name__ == "__main__":
    listings = main()
    for listing in listings:
        listing.save_listing()
    for index, listing in enumerate(listings):
        listing.print_label(index + 1)
