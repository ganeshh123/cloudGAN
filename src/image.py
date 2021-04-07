import os
import numpy as np
import xarray as xr
from scipy.interpolate import RectBivariateSpline

class Regrid:
    """ Class to perform regriding between different resolutions
    """

    def __init__(self, grid_a, grid_b):
        """Create a regridding object

        Args:
            grid_a: dataset in the resolution to regrid to
            grid_b: dataset in the resolution to regrid from.
        """
        if grid_a.start_offset == grid_b.start_offset:
            start_offset = 0.0
        else:
            start_offset = grid_a.start_offset * float(grid_a.resolution.split()[2]) / float(grid_b.resolution.split()[2]) - grid_b.start_offset

        x = (np.array(range(grid_a.dims['columns'])) - grid_a.track_offset) * float(grid_a.resolution.split()[1]) / float(grid_b.resolution.split()[1]) + grid_b.track_offset
        y = np.array(range(grid_a.dims['rows'])) * float(grid_a.resolution.split()[2]) / float(grid_b.resolution.split()[2]) + start_offset

        self._x = x
        self._y = y

        self._rows = grid_b.dims['rows']
        self._cols = grid_b.dims['columns']

    def regrid_channel(self, grid):
        f = RectBivariateSpline(np.arange(self._rows),
                                           np.arange(self._cols),
                                           grid[:])
        values = f(self._y, self._x)
        return (('rows', 'columns'), values)

    def __call__(self, dataset):
        """Regrid `dataset` to the resolution defined by this object"""
        channels = {}
        for name in dataset:
            channels[name] = self.regrid_channel(dataset[name])

        return xr.Dataset(channels)


class ImageLoader:
    """Class to load Sentinel-3 SLSTR level 1 product data"""

    def __init__(self, path):
        """Create a new product loader

        Args:
            path: file location of the product
        """
        self.path = path

    def load_radiances(self, view='an'):
        """Load the radiance channels

        Data will be returned in the 0.5km grid resolution.

        Args:
            view: what view to load radiances in e.g. 'an', 'ao' etc.
        """
        rads = [
            self.load_radiance_channel(
                self.path,
                i,
                view) for i in range(
                1,
                7)]
        attrs = rads[0].attrs
        rads = xr.merge(rads)
        rads.attrs['start_offset'] = attrs['start_offset']
        rads.attrs['track_offset'] = attrs['track_offset']
        rads.attrs['resolution'] = attrs['resolution']
        return rads

    def load_irradiances(self, view='an'):
        """Load the irradiances

        Data will be returned in the 0.5km grid resolution.

        Args:
            view: what view to load radiances in e.g. 'an', 'ao' etc.
        """
        irradiances = {}
        for i in range(1, 7):
            name = 'S{}_solar_irradiance_{}'.format(i, view)
            file_name = os.path.join(
                self.path, 'S{}_quality_{}.nc'.format(
                    i, view))
            irradiance = xr.open_dataset(file_name, engine='h5netcdf')[name][:].data[0]
            irradiances[name] = irradiance
        return irradiances


    def load_reflectances(self, view='an'):
        """Load the reflectances

        This will first load the radiances, then convert them to reflectance
        values using the solar zenith and irradiance.

        Data will be returned in the 0.5km grid resolution.

        Args:
            view: what view to load reflectances in e.g. 'an', 'ao' etc.
        """
        refs = [
            self.load_reflectance_channel(
                self.path,
                i,
                view) for i in range(
                1,
                7)]
        attrs = refs[0].attrs
        refs = xr.merge(refs)
        refs.attrs['start_offset'] = attrs['start_offset']
        refs.attrs['track_offset'] = attrs['track_offset']
        refs.attrs['resolution'] = attrs['resolution']
        return refs

    def load_bts(self, view='in'):
        """Load the brightness temperatures

        Data will be returned in the 1km grid resolution.

        Args:
            view: what view to load brightness temps in e.g. 'in', 'io' etc.
        """
        bts = [self.load_bt_channel(self.path, i, view) for i in range(7, 10)]
        attrs = bts[0].attrs
        bts = xr.merge(bts)
        bts.attrs['start_offset'] = attrs['start_offset']
        bts.attrs['track_offset'] = attrs['track_offset']
        bts.attrs['resolution'] = attrs['resolution']
        return bts

    def load_flags(self, view='in'):
        """Load flags for this product.

        This will include entries such whether the pixels are land, ocean,
        twilight, day etc.

        Data will be returned in the 1km grid resolution.

        Args:
            view: what view to load flags in e.g. 'in', 'io' etc.
        """
        flags_path = os.path.join(self.path, 'flags_{}.nc'.format(view))
        excluded = [
            'confidence_orphan_{}',
            'pointing_orphan_{}',
            'pointing_{}',
            'cloud_orphan_{}',
            'bayes_orphan_{}',
            'probability_cloud_dual_{}']
        excluded = [e.format(view) for e in excluded]
        flags = xr.open_dataset(flags_path, decode_times=False,
                                drop_variables=excluded, engine='h5netcdf')

        confidence_var = 'confidence_{}'.format(view)
        flag_masks = flags[confidence_var].attrs['flag_masks']
        flag_meanings = flags[confidence_var].attrs['flag_meanings'].split()
        flag_map = dict(zip(flag_meanings, flag_masks))
        expanded_flags = {}
        for key, bit in flag_map.items():
            msk = flags[confidence_var] & bit
            msk = xr.where(msk > 0, 1, 0)
            expanded_flags[key] = msk
        flags = flags.assign(**expanded_flags)
        return flags

    def load_geometry(self):
        """Load geometry information for this product.

        Data will be returned in the 1km grid resolution.

        Args:
            view: what view to load geometry in e.g. 'in', 'io' etc.
        """
        path = os.path.join(self.path, 'geometry_tn.nc')
        geo = xr.open_dataset(path, decode_times=False, engine='h5netcdf')
        return geo

    def load_met(self):
        """Load meterological information for this product.

        Data will be returned in the 1km grid resolution.

        Args:
            view: what view to load metreological in e.g. 'in', 'io' etc.
        """
        met_path = os.path.join(self.path, 'met_tx.nc')
        met = xr.open_dataset(met_path, decode_times=False, engine='h5netcdf')
        met = met[['total_column_water_vapour_tx', 'cloud_fraction_tx',
                   'skin_temperature_tx', 'sea_surface_temperature_tx',
                   'total_column_ozone_tx', 'soil_wetness_tx',
                   'snow_albedo_tx', 'snow_depth_tx', 'sea_ice_fraction_tx',
                   'surface_pressure_tx']]
        met = met.squeeze()
        return met

    def load_geodetic(self, view='an'):
        """Load geodetic information for this product.

        Data will be returned in the 1km grid resolution.

        Args:
            view: what view to load geodetic in e.g. 'in', 'io' etc.
        """
        flags_path = os.path.join(self.path, 'geodetic_{}.nc'.format(view))
        excluded = ['elevation_orphan_an', 'elevation_an',
                    'latitude_orphan_an', 'longitude_orphan_an']
        flags = xr.open_dataset(flags_path, decode_times=False,
                                drop_variables=excluded, engine='h5netcdf')
        return flags

    def load_reflectance_channel(self, path, channel_num, view='an'):
        rads = self.load_radiance_channel(path, channel_num, view)
        names = {name: name.replace('radiance', 'reflectance')
                 for name in rads}
        rads = rads.rename(names)
        irradiances = self.load_irradiances(view)
        geometry = self.load_geometry()

        solar_zenith = geometry.solar_zenith_tn[:]
        solar_zenith = np.nan_to_num(solar_zenith, 0.0)

        regridder = Regrid(rads, geometry)
        solar_zenith = regridder.regrid_channel(solar_zenith)[1]

        DTOR = 0.017453292
        mu0 = np.where(solar_zenith < 90, np.cos(DTOR * solar_zenith), 1.0)

        name = 'S{}_reflectance_{}'.format(channel_num, view)
        rads[name] = rads[name] / \
            (irradiances[name[:2] + '_solar_irradiance_{}'.format(view)] * mu0) * np.pi
        return rads

    def load_radiance_channel(self, path, channel_num, view='an'):
        excluded_vars = [
            "S{}_exception_{}".format(channel_num, view),
            "S{}_radiance_orphan_{}".format(channel_num, view),
            "S{}_exception_orphan_{}".format(channel_num, view)
        ]

        path = os.path.join(
            path, 'S{}_radiance_{}.nc'.format(
                channel_num, view))
        radiance = xr.open_dataset(
            path, decode_times=False, drop_variables=excluded_vars, engine='h5netcdf')
        return radiance


    def load_bt_channel(self, path, channel_num, view='in'):
        excluded_vars = [
            "S{}_exception_{}".format(channel_num, view),
            "S{}_BT_orphan_{}".format(channel_num, view),
            "S{}_exception_orphan_{}".format(channel_num, view)
        ]

        path = os.path.join(path, 'S{}_BT_{}.nc'.format(channel_num, view))
        bt = xr.open_dataset(path, decode_times=False,
                             drop_variables=excluded_vars, engine='h5netcdf')
        return bt
