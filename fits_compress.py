from astropy.io import fits
import sys

def read_fits_file(filename):
    """Open a .fits file.
       Return the hdulist
    """

    # Open the file
    try:
        return fits.open(filename)

    except IOError:
        print("Could not read file:", filename)
        sys.exit(1)


def write_fits_file(hdulist, filename='out.fits'):
    """Create a new fits object from data and headers, and write to file."""
    
    # Write to file
    hdulist.writeto(filename, overwrite=True)
    hdulist.close()


def decompress_fits(hdulist):
    new_hdulist = [hdulist[0]]
    
    for h in hdulist[1:]:
        new_hdu = fits.ImageHDU(h.data, header=h.header)
        
        new_hdulist.append(new_hdu)
        
    return fits.HDUList(new_hdulist)
    
    
def compress_fits(hdulist):
    new_hdulist = []
    
    for h in hdulist:
        if type(h) == fits.PrimaryHDU:
            if h.data is not None:
                new_hdulist.append(fits.PrimaryHDU(None, header=h.header))
                new_hdulist.append(fits.CompImageHDU(h.data, header=h.header))
            else:
                new_hdulist.append(h)
        
        elif type(h) == fits.ImageHDU:
            new_hdu = fits.CompImageHDU(h.data, header=h.header)
            new_hdulist.append(new_hdu)
        else:
            new_hdulist.append(h)
        
    return fits.HDUList(new_hdulist)
    

if __name__ == "__main__":
    args = sys.argv[1:]
    
    fname = args[0]
    original = read_fits_file(fname)
    
    if fname.split(".")[-1] == "fz":
        new_hdul = decompress_fits(original)
        new_fname = ".".join(fname.split(".")[:-1])
    else:
        new_hdul = compress_fits(original)
        new_fname = fname + ".fz"
    
    write_fits_file(new_hdul, new_fname)
        
