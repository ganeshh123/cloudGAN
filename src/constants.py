RADIANCE_CHANNELS = [
    'S1_radiance_an',
    'S2_radiance_an',
    'S3_radiance_an',
    'S4_radiance_an',
    'S5_radiance_an',
    'S6_radiance_an'
]

REFLECTANCE_CHANNELS = [
    'S{}_reflectance_an'.format(i) for i in range(
        1, 7)]

BT_CHANNELS = [
    'S7_BT_in',
    'S8_BT_in',
    'S9_BT_in'
]

IMG_CHANNELS = RADIANCE_CHANNELS.copy()
IMG_CHANNELS.extend(BT_CHANNELS)

RESOLUTION_1KM = (1200, 1500)

NADIR_1KM = (548, 52)
OBLIQUE_1KM = (50, -50)

BORDER_OFFSET = 20
