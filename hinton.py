import numpy as N
import pylab as P

def _blob(x,y,area,colour):
    """
    Draws a square-shaped blob with the given area (< 1) at
    the given coordinates.
    """
    hs = N.sqrt(area) / 2
    xcorners = N.array([x - hs, x + hs, x + hs, x - hs])
    ycorners = N.array([y - hs, y - hs, y + hs, y + hs])
    P.fill(xcorners, ycorners, colour, edgecolor=colour)

def hinton(W, labels, lines = True, maxWeight=None, fontsize = 16):
    """
    Draws a Hinton diagram for visualizing a weight matrix. 
    Temporarily disables matplotlib interactive mode if it is on, 
    otherwise this takes forever.
    """
    reenable = False
    if P.isinteractive():
        P.ioff()
    P.clf()
    height, width = W.shape
    if not maxWeight:
        maxWeight = 2**N.ceil(N.log(N.max(N.abs(W)))/N.log(2))

    P.fill(N.array([0,width,width,0]),N.array([0,0,height,height]),'gray')
    P.axis('off')
    P.axis('equal')
    P.text(-0.75, height+0.2, 'Scena', {'fontsize': fontsize})
    P.text(-0.75, height-0.1, 'Model', {'fontsize': fontsize})
    for y in xrange(height):
        label = labels[height-y-1]
        x = -0.5
        if len(label) > 2:
            x = -0.5 - 0.05*(len(label))
        P.text(x, y+0.5, label, {'fontsize': 15})
        if lines: 
            P.axhline(y, color='k', xmin=0.11, xmax=0.89)
    for x in xrange(width):
        _x = x+0.5
        if len(labels[x]):
            _x -= 0.05*(len(labels[x]))
        P.text(_x, height+0.2, labels[x], {'fontsize': fontsize})
        if lines:
            P.axvline(x, color='k')
        for y in xrange(height):
            _x = x+1
            _y = y+1
            w = W[y,x]
            if w > 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1,w/maxWeight),'white')
            elif w < 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1,-w/maxWeight),'black')
            P.text(_x - 0.67, height - _y + 0.5, '{0:.0%}'.format(w), {'fontsize': fontsize})
    if reenable:
        P.ion()
    P.show()



if __name__ == "__main__":
    #EXAMPLE
    W1 = N.random.rand(5, 5) 

    W2 =N.array([           [0.0, 0, 0, 0, 0],
			    [0, 0.08, 0, 0, 0],
			    [0, 0, 0, 0, 0],
			    [0, 0, 0, 0.35, 0],
                            [0, 0, 0, 0, 0.42]])
                        
    labels = N.array([ 'label1', 'label2', 'label3', 'label4', 'label15'])
    hinton(W1, labels)
