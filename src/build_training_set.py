import sys
from pathlib import Path

open(Path(sys.path[0]).resolve() / 'data_store' / 'searchResults.txt', 'w').close()

from copernicus_search.copernicus_search import copernicus_search
from copernicus_download.copernicus_download import copernicus_download
from unzip_images.unzip_images import unzip_images
from build_rgb_images.build_rgb_images import build_rgb_images
from build_images.build_mask_images import build_mask_images
from slice_image.slice_images import slice_images
from sort_data.get_mask_files import get_mask_files
from sort_data.sort_tiles import sort_tiles

numberOfResults = 25
filterTagName = 'sentinel3:cloudypixels'
filterAttribute = 'percentage'
filterMin = 0
filterMax = 50
filterDateRange = '2020-06-01T00:00:00.000Z TO NOW'

print('\n\n---- BUILDING TRAINING SET ----')
print('\n\n\n')
#urls = copernicus_search(numberOfResults, filterTagName, filterAttribute, filterMin, filterMax, filterDateRange)
print('\n\n\n')
#copernicus_download(urls)
print('\n\n\n')
imagePaths = unzip_images()
#print('\n\n\n')
build_rgb_images()
build_mask_images()
slice_images()
maskFiles = get_mask_files()
sort_tiles(maskFiles)


print('\n\n---- COMPLETED ----')