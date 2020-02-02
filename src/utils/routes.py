

def encode_coords(coords, prev_lat=0, prev_lng=0):
    '''Encodes a polyline using Google's polyline algorithm
       
    :param coords: Coordinates to transform (list of tuples in order: latitude, 
    longitude).
    :type coords: list
    :returns: Google-encoded polyline string.
    :rtype: string    
    '''
     
    result = []
     
    x,y = coords
            
    lat, lng = int(x * 1e5), int(y * 1e5)
    prev_lat, prev_lng = int(prev_lat * 1e5), int(prev_lng * 1e5)
    

    d_lat = _encode_value(lat - prev_lat)
    d_lng = _encode_value(lng - prev_lng)        

    prev_lat, prev_lng = lat, lng

    result.append(d_lat)
    result.append(d_lng)

    return ''.join(c for r in result for c in r)
     
def _split_into_chunks(value):
    while value >= 32: #2^5, while there are at least 5 bits
         
        # first & with 2^5-1, zeros out all the bits other than the first five
        # then OR with 0x20 if another bit chunk follows
        yield (value & 31) | 0x20
        value >>= 5
    yield value
 
def _encode_value(value):
    # Step 2 & 4
    value = ~(value << 1) if value < 0 else (value << 1)
     
    # Step 5 - 8
    chunks = _split_into_chunks(value)
     
    # Step 9-10
    return (chr(chunk + 63) for chunk in chunks)

