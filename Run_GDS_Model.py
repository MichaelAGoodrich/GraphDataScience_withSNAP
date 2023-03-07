""" Create a small labeled graph from the Stanford Network Repository.
    I can't get the SNAP.py tools to install and it appears that they are
    not maintained anymore since the last update was December 2020.

    So, load a lablelled data set and trye to do some graph data science
    on it. Try https://snap.stanford.edu/data/amazon-meta.html

    J. Leskovec, L. Adamic and B. Adamic. The Dynamics of Viral Marketing. 
    ACM Transactions on the Web (ACM TWEB), 1(1), 2007.

    Michael A. Goodrich
    Brigham Young University

    March 2023    
"""

def main():
    status = False
    try:
        import snap
        version = snap.Version
        i = snap.TInt(5)
        if i == 5:
            status = True
    except:
        pass

    if status:
        print("SUCCESS, your version of Snap.py is %s" % (version))
    else:
        print("*** ERROR, no working Snap.py was found on your computer")


main()