from wrappers import leastsquareslinefit

# compute_error functions

def sumsquared_error(sequence, segment):
    """Return the sum of squared errors for a least squares line fit of one segment of a sequence"""
    x0,y0,x1,y1 = segment
    p, error = leastsquareslinefit(sequence,(x0,x1))
    return error
    
# create_segment functions

def regression(sequence, seq_range):
    """Return (x0,y0,x1,y1) of a line fit to a segment of a sequence using linear regression"""
    p, error = leastsquareslinefit(sequence,seq_range)
    y0 = p[0]*seq_range[0] + p[1]
    y1 = p[0]*seq_range[1] + p[1]
    return (seq_range[0],y0,seq_range[1],y1)
    
def interpolate(sequence, seq_range):
    """Return (x0,y0,x1,y1) of a line fit to a segment using a simple interpolation"""
    return (seq_range[0], sequence[seq_range[0]], seq_range[1], sequence[seq_range[1]])
