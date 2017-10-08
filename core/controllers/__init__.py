import os
import glob

# This trick overrides the controller modules __all__ attribute and includes
# the modules inside the controllers path
__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]