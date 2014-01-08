#!/usr/bin/python

# Assuming speed of aging whiskey is proportional to the amount of oak surface
# area per volume of liquid, calculate the relative rates of aging for various
# sizes of barrels.
# The main assumption is oversimplifiying the aging process, but still a useful
# metric for "oakiness".    Aaron Fabbri  2011.

# volumes of barrels in gallons.  First is standard whiskey barrel 53 gal.
vol_list = [53, 8, 6.6, 6, 5.3, 2.7]

def cu_in_to_gal(i) :	return (i * 0.00433) 
def gal_to_cu_in(g) :	return (g/0.00433)

def h_by_vol(v) :	return (v/0.269)**(1/3.0)

def r_by_vol(v) : 	return (v/10.773)**(1/3.0)

pi = 3.1415927
def surf_by_vol_gal(g) :
	v = (gal_to_cu_in(float(g)))
	r = r_by_vol(v)
	h = h_by_vol(v)
	val = 2 * pi * r * (r + h)
	return val


def main( ) :
	ratio_53_gal = surf_by_vol_gal(vol_list[0])/vol_list[0]
	for v in vol_list :
		sa = surf_by_vol_gal(v)
		print "A %.1f gal barrel, approx  surf. area %.1f in^3., "\
			"ratio %.1f" % ( v, sa, sa/v) 

		if (v != vol_list[0]) :
			print "  -> %.1f gal barrel is %.1fx faster " \
				"than 53 gal"  % (v, ((sa/v)/ratio_53_gal))

if __name__ == "__main__":
	main()


